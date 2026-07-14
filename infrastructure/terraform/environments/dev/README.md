# Dev Environment

Terraform environment for the portfolio lab's first AWS foundation.

## Resources

This environment provisions:

- DynamoDB table for health reports
- encrypted, versioned S3 bucket for backups
- SNS topic for alerts
- optional email subscription
- CloudWatch log groups reserved for later Lambda and monitoring jobs

## Prerequisites

Install:

- Terraform
- AWS CLI

Configure AWS credentials outside the repository:

```bash
aws configure
```

Do not commit credentials, `terraform.tfvars`, generated plans, or Terraform state.

## Configure

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

- set `backup_bucket_name` to a globally unique bucket name
- optionally set `alert_email`
- confirm `aws_region`

## Validate

```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan
```

Review the plan carefully before applying. This repository intentionally does not include a Makefile target for `terraform apply`.

## Destroy

When tearing down the lab:

```bash
terraform plan -destroy
terraform destroy
```

Review the destroy plan before approving it. If `backup_bucket_force_destroy` is `false`, the S3 bucket must be empty before Terraform can delete it.
