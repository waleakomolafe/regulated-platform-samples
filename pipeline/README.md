# The regulated-deploy pipeline template

`templates/regulated-deploy.yml` is a reusable workflow that deploys a
Terraform module the way a regulated change process requires: approved
before it runs, federated while it runs, evidenced after it runs.

The three controls, and where each lives:

| control | where it lives | why there |
|---|---|---|
| approval | the GitHub **environment's** protection rules | the gate must not be in the same file a PR can change — the template cannot bypass its own approval |
| cloud credentials | **OIDC federation** (`id-token: write` + `azure/login`) | no stored secret exists, so none can leak, rotate-wrong, or appear in a log |
| change evidence | **artifacts**: the plan before, the apply log after | the auditor's question — "show me what changed and who approved it" — is answered by the run itself |

Configuration the caller sets once (environment variables on the GitHub
environment — public, non-secret values): `ARM_CLIENT_ID`,
`ARM_TENANT_ID`, `ARM_SUBSCRIPTION_ID`. On the Azure side, one federated
credential trusts this workflow; see `docs/decisions/0003` for why this
beats a stored client secret in every dimension an auditor cares about.

## The gate that audits the gate

`../tools/check_pipeline_template.py` runs in CI and fails the build if
the template ever regresses: OIDC permission missing, a stored cloud
secret reintroduced, the environment gate removed, evidence uploads
dropped, an action pin going soft, or `pull_request_target` with
PR-derived expressions. The template lives outside `.github/workflows`,
so pipeline-sentinel never executes it — this checker is its auditor.

Worth knowing (it is in the checker's source too): the first version of
that checker was blind — it regexed the stringified job dict, the quote
in `uses':` defeated the pattern, and a 42-character typo'd SHA passed a
pin check that never looked at a single action. The checker now walks the
parsed structure. A gate that has never failed is not yet known to be a
gate; this one failed, was fixed, and is negative-tested.
