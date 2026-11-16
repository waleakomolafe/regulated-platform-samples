# regulated-platform-samples

Work samples for platform engineering in **regulated financial services**.
Generic artifacts — no employer code, no client data — that demonstrate the
craft the way it is actually practiced under a regulator: controls carried
inside the artifact, not bolted on by a document nobody opens.

The repository grows. Roughly one increment per week: a module, a pipeline
template, a runbook, a set of decision records, a query pack. Each
increment is tagged, logged in the CHANGELOG, and validated in CI. The
history is the point — platform engineering is continuous, and a sample
that never changes proves nothing about how it is maintained.

## What is here

| artifact | status | the control it demonstrates |
|---|---|---|
| `terraform/modules/secure-storage` | **v0.1** | governance carried inside the module: private-only, Entra-only auth, versioning, TLS floor, mandatory tags with validation |
| `docs/decisions` | **v0.1** | decision records in a fixed format — the reasoning auditors and reviewers actually ask for |
| `pipeline/` | **v0.2** | the regulated-deploy template: approval via environments, OIDC federation, change evidence as artifacts — audited by its own structural gate |
| `runbooks/` | **v0.3** | the template (verification-shaped) + a worked example — restore a deleted blob — validated by [runbook-doctor](https://github.com/waleakomolafe/runbook-doctor) |
| `queries/` | planned v0.5 | KQL / PromQL pack, each query annotated with the control it evidences |

## The financial-services framing

Everything here is written the way regulated work is written:

- **Evidence over assertion.** A control that exists only in a README is a
  claim; these artifacts carry the control in code where a reviewer (or an
  auditor) can read it.
- **Change is gated.** Pull requests, review, environments, approvals —
  the samples model the four-eyes pattern banks require.
- **No invented compliance.** Nothing here claims certification. Where a
  control pattern matches PCI-style or regulator expectations, the README
  says "designed for this class of control," and points at the lines.

## Validation

CI runs on every push: `terraform fmt -check` and `terraform validate` on
every module, markdown checks, and the workflows are audited by
[pipeline-sentinel](https://github.com/waleakomolafe/pipeline-sentinel) —
the same auditor described in `docs/decisions/0002`.

## Related work

The tooling repos this samples lane uses and references:
[drift-sentinel](https://github.com/waleakomolafe/drift-sentinel) (Terraform
drift that opens a pull request),
[slo-sentinel](https://github.com/waleakomolafe/slo-sentinel) (error-budget
alerting from a spec),
[pipeline-sentinel](https://github.com/waleakomolafe/pipeline-sentinel)
(workflow auditing),
[runbook-doctor](https://github.com/waleakomolafe/runbook-doctor) (runbook
staleness gate).

## License

MIT
