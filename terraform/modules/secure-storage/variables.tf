variable "name" {
  description = "Storage account name (3-24 lowercase letters/digits). Globally unique in Azure."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.name))
    error_message = "storage account name must be 3-24 lowercase alphanumeric characters"
  }
}

variable "resource_group_name" {
  description = "Resource group to deploy into."
  type        = string
}

variable "location" {
  description = "Azure region."
  type        = string
}

variable "owner" {
  description = "Accountable team or person. Auditors ask 'who owns this'; the tag answers before they do."
  type        = string

  validation {
    condition     = length(var.owner) > 0
    error_message = "owner tag is mandatory - an unowned resource does not pass change review"
  }
}

variable "cost_centre" {
  description = "Cost centre code for showback/chargeback."
  type        = string

  validation {
    condition     = can(regex("^CC-[0-9]{3,6}$", var.cost_centre))
    error_message = "cost_centre must match CC-<digits> (e.g. CC-4471)"
  }
}

variable "data_classification" {
  description = "Classification from the data policy. Free-text classifications are how 'internal-ish' happens."
  type        = string

  validation {
    condition     = contains(["public", "internal", "confidential", "restricted"], var.data_classification)
    error_message = "data_classification must be one of: public, internal, confidential, restricted"
  }
}

variable "tags" {
  description = "Additional tags. owner/cost_centre/data_classification are set separately and cannot be overridden here."
  type        = map(string)
  default     = {}
}

variable "retention_days" {
  description = "Blob soft-delete retention. Regulated deletions must be recoverable; 30 is the floor."
  type        = number
  default     = 30

  validation {
    condition     = var.retention_days >= 30
    error_message = "retention below 30 days does not meet the recoverability floor for regulated data"
  }
}
