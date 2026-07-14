locals {
  name_prefix = "${var.project_name}-${var.environment}"

  common_tags = {
    Project     = "Terraform-Managed Hybrid Infrastructure Lab"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Repository  = "terraform-hybrid-infrastructure-lab"
  }
}
