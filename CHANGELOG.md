# Changelog

All notable changes to this repository. The repository grows in tagged
increments; this file is the map.

## v0.1.0 — 2026-11-12

First increment.

- `terraform/modules/secure-storage`: an Azure storage module with the
  governance carried inside — no public network access, Entra-only auth
  (shared keys disabled), infrastructure encryption, blob versioning,
  TLS 1.2 minimum, mandatory tags with variable validation.
- `docs/decisions/0001`: why the module refuses shared-key auth.
- `docs/decisions/0002`: why this repository audits its own workflows.
- CI: terraform fmt/validate per module, markdown checks, workflow audit
  by pipeline-sentinel.

## Planned

- v0.2 — `pipeline/`: reusable YAML template with approval gates,
  environments, OIDC federation, and the evidence a change process needs.
- v0.3 — `runbooks/`: skeleton + one worked example, validated by
  runbook-doctor in CI.
- v0.4 — `docs/decisions` grows: OIDC over stored secrets, deny-by-default
  egress, change approval via pull request instead of a CAB ticket.
- v0.5 — `queries/`: KQL and PromQL pack, each query annotated with the
  control it evidences.
