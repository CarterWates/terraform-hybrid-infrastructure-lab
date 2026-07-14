variable "aws_region" {
  description = "AWS region for the dev environment."
  type        = string
  default     = "us-east-1"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]$", var.aws_region))
    error_message = "aws_region must look like us-east-1."
  }
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev"], var.environment)
    error_message = "Only the dev environment is supported in this lab phase."
  }
}

variable "project_name" {
  description = "Project name used for tags and resource names."
  type        = string
  default     = "hybrid-lab"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,30}$", var.project_name))
    error_message = "project_name must be 3-31 lowercase letters, numbers, or hyphens and start with a letter."
  }
}

variable "health_table_name" {
  description = "DynamoDB table name for node health reports."
  type        = string
  default     = "HybridLabHealth"

  validation {
    condition     = can(regex("^[A-Za-z0-9_.-]{3,255}$", var.health_table_name))
    error_message = "health_table_name must be a valid DynamoDB table name."
  }
}

variable "enable_health_ttl" {
  description = "Enable TTL for health records."
  type        = bool
  default     = false
}

variable "health_ttl_attribute" {
  description = "DynamoDB attribute name used for TTL when enabled."
  type        = string
  default     = "expiresAt"

  validation {
    condition     = can(regex("^[A-Za-z][A-Za-z0-9_]{0,254}$", var.health_ttl_attribute))
    error_message = "health_ttl_attribute must start with a letter and contain only letters, numbers, or underscores."
  }
}

variable "backup_bucket_name" {
  description = "Globally unique S3 bucket name for encrypted configuration backups."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$", var.backup_bucket_name))
    error_message = "backup_bucket_name must be a valid S3 bucket name."
  }
}

variable "backup_bucket_force_destroy" {
  description = "Allow Terraform to delete the backup bucket even when it contains objects. Keep false unless intentionally tearing down a disposable lab."
  type        = bool
  default     = false
}

variable "backup_lifecycle_transition_days" {
  description = "Days before backup objects transition to infrequent access storage."
  type        = number
  default     = 30

  validation {
    condition     = var.backup_lifecycle_transition_days >= 30
    error_message = "backup_lifecycle_transition_days must be at least 30."
  }
}

variable "backup_lifecycle_expiration_days" {
  description = "Days before backup objects expire."
  type        = number
  default     = 365

  validation {
    condition     = var.backup_lifecycle_expiration_days >= 90
    error_message = "backup_lifecycle_expiration_days must be at least 90."
  }
}

variable "alert_email" {
  description = "Optional email address for SNS alert subscription. Leave empty to skip email subscription."
  type        = string
  default     = ""

  validation {
    condition     = var.alert_email == "" || can(regex("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", var.alert_email))
    error_message = "alert_email must be empty or a valid email address."
  }
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days."
  type        = number
  default     = 14

  validation {
    condition     = contains([7, 14, 30, 60, 90, 120, 150, 180, 365], var.log_retention_days)
    error_message = "log_retention_days must be a standard CloudWatch retention value."
  }
}
