output "id" {
  description = "Storage account resource id."
  value       = azurerm_storage_account.this.id
}

output "name" {
  description = "Storage account name."
  value       = azurerm_storage_account.this.name
}

output "primary_endpoint" {
  description = "Blob endpoint. Reachable only over private endpoints - the public flag is off."
  value       = azurerm_storage_account.this.primary_blob_endpoint
}

output "data_classification" {
  description = "The classification this account carries, for downstream evidence tooling."
  value       = var.data_classification
}
