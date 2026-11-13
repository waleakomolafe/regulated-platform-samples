# Secure storage module (Azure)

A storage account module where the regulated-financial defaults are
**carried inside**: there is no configuration in which this module deploys
a publicly reachable storage account, an account that accepts shared-key
auth, or an untagged resource. The governance is not a wiki page next to
the module — it is the module.

What the module enforces, and how a reviewer checks it:

| control | where | what it means in a regulated environment |
|---|---|---|
| No public network access | `public_network_access_enabled = false` | the account is reachable only through private endpoints / approved networks |
| Shared key auth disabled | `shared_access_key_enabled = false` | access is Entra identities only — no long-lived keys to leak or rotate |
| Infrastructure encryption | `infrastructure_encryption_enabled = true` | double encryption at rest, including the platform's own |
| Blob versioning + PITT | `blob_properties` | deletion and overwrite are recoverable — the change-management story |
| TLS 1.2 minimum | `min_tls_version` | the crypto floor is a module constant, not a per-deployment choice |
| Mandatory tags with validation | `variables.tf` | owner / cost-centre / data-classification must exist and validate BEFORE apply |
| No arbitrary data classification | variable validation | only the classification levels the data policy recognises |

## Use

    module "evidence_store" {
      source = "./terraform/modules/secure-storage"

      name                = "evstoreprod01"
      resource_group_name = "rg-evidence-prod"
      location            = "westeurope"

      owner              = "platform-engineering"
      cost_centre        = "CC-4471"
      data_classification = "confidential"

      tags = { application = "evidence-store" }
    }

Deploy a public or key-auth account with this module and the plan fails in
`terraform validate` / `plan` — the reviewer never has to be the one who
catches it.

## Why these choices

See `docs/decisions/0001` (why shared-key auth is refused outright) and
`docs/decisions/0002` (why this repository audits its own CI).
