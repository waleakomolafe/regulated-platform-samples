#!/usr/bin/env python3
"""Structural gate for the regulated-deploy template.

The template under pipeline/templates/ is not executed by GitHub (it lives
outside .github/workflows), so pipeline-sentinel never sees it. This gate
is its auditor: it fails the build when any governance fact of the
regulated-deploy template regresses.

Checked facts (each one is a control a regulated change process needs):

  1. OIDC, not stored cloud credentials: `permissions` carries
     id-token: write, and NO stored cloud secret name appears anywhere
     (AZURE_CLIENT_SECRET, AWS_SECRET_ACCESS_KEY, ...).
  2. The deploy job runs in an `environment:` — the approval gate lives
     in the environment's protection rules, not in the template.
  3. Evidence is produced: at least two upload-artifact steps (the plan
     before, the apply log after).
  4. Every third-party action is pinned to a full 40-hex commit SHA.
  5. Cloud config uses `vars.`, never `secrets.` — federation means there
     is no secret to read.
  6. No pull_request_target trigger with PR-derived expressions (the
     classic fork-code-with-repo-secrets footgun).

Exit 0 clean, 1 findings, 2 unreadable file.
"""

import re
import sys
from pathlib import Path

import yaml

SHA = re.compile(r"^[0-9a-f]{40}$")
STORED_CLOUD_SECRET = re.compile(
    r"secrets\.(AZURE_CLIENT_SECRET|AZURE_CLIENT_ID|AWS_SECRET_ACCESS_KEY|"
    r"AWS_ACCESS_KEY_ID|AWS_SESSION_TOKEN|GCP_SA_KEY|GOOGLE_CREDENTIALS)",
    re.IGNORECASE,
)


def check(path: str) -> list:
    p = Path(path)
    findings = []
    try:
        raw = p.read_text(encoding="utf-8")
        doc = yaml.safe_load(raw)
    except Exception as exc:
        print(f"FAIL cannot read/parse {path}: {exc}")
        sys.exit(2)

    perms = doc.get("permissions") or {}
    if perms.get("id-token") != "write":
        findings.append("permissions.id-token is not write - OIDC federation "
                        "cannot mint a token without it")

    m = STORED_CLOUD_SECRET.search(raw)
    if m:
        findings.append(f"stored cloud credential referenced: {m.group(0)} - "
                        "federation means there is no secret to store")

    jobs = doc.get("jobs") or {}
    env_jobs = [name for name, j in (jobs or {}).items()
                if isinstance(j, dict) and j.get("environment")]
    if not env_jobs:
        findings.append("no job runs in an environment: - the approval gate "
                        "must live in the environment's protection rules")

    # Walk the PARSED steps, never str(dict): the stringified form renders
    # `uses':` with a quote before the colon, a uses-regex matches nothing,
    # and the pin check goes quietly blind. Found the hard way, 2026-11-16:
    # a 42-character typo'd SHA passed this gate because the gate never
    # actually looked at a single action.
    uses = []
    for j in jobs.values():
        if not isinstance(j, dict):
            continue
        for st in (j.get("steps") or []):
            if isinstance(st, dict) and isinstance(st.get("uses"), str):
                uses.append(st["uses"])
    for u in uses:
        if u.startswith(("./", "docker://")):
            continue
        ref = u.rsplit("@", 1)[-1]
        if not SHA.match(ref):
            findings.append(f"third-party action not SHA-pinned: {u}")

    if sum(1 for u in uses if u.startswith("actions/upload-artifact@")) < 2:
        findings.append("expected at least 2 evidence uploads (plan + apply "
                        "log), found "
                        + str(sum(1 for u in uses if u.startswith("actions/upload-artifact@"))))

    if re.search(r"secrets\.ARM_", raw):
        findings.append("ARM_* values come from vars. (public config) - "
                        "reading them from secrets. reintroduces a stored "
                        "credential")

    trig = doc.get("on", doc.get(True)) or {}
    trig_keys = list(trig) if isinstance(trig, dict) else (
        [trig] if isinstance(trig, str) else list(trig or []))
    if "pull_request_target" in trig_keys:
        if re.search(r"github\.event\.pull_request", raw):
            findings.append("pull_request_target with PR-derived expressions: "
                            "fork-controlled code with repository context")

    return findings


def main() -> int:
    targets = sys.argv[1:] or ["pipeline/templates/regulated-deploy.yml"]
    bad = 0
    for t in targets:
        for f in check(t):
            print(f"FAIL {t}: {f}")
            bad += 1
    if not bad:
        n = len(targets)
        print(f"pipeline template gate: {n} template(s) carry all governance "
              f"facts (OIDC, environment gate, evidence, SHA pins)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
