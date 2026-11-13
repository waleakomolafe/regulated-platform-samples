# The controls in this file are not configurable where configurability
# would defeat them. A regulated storage account has exactly one shape:
# private, identity-only, double-encrypted, versioned, TLS 1.2 minimum.
# Deploys that need something else need a different module - and a
# conversation, not a boolean.

resource "azurerm_storage_account" "this" {
  name                     = var.name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  # Public reachability is the defect every storage review finds.
  public_network_access_enabled = false

  # No shared keys: access is Entra identities (RBAC) only. There is no
  # key to leak, rotate, or find in a CI log six months from now.
  shared_access_key_enabled = false

  # The platform's own encryption layer, beneath any CMK the deployment adds.
  infrastructure_encryption_enabled = true

  min_tls_version = "TLS1_2"

  # Regulated deletions are recoverable deletions.
  blob_properties {
    versioning_enabled = true
    delete_retention_policy {
      days = var.retention_days
    }
  }

  tags = merge(
    {
      owner               = var.owner
      cost_centre         = var.cost_centre
      data_classification = var.data_classification
      managed_by          = "terraform"
    },
    var.tags,
  )
}
