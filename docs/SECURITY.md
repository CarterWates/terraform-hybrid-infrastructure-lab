# Security Notes

This project is designed as a public portfolio repository, so the default posture is conservative.

## Never Commit

- AWS access keys or session tokens
- `.env` files
- Terraform state or plan files containing sensitive values
- `terraform.tfvars`
- private keys, certificates, or SSH material
- generated backup archives
- screenshots with account IDs, emails, private URLs, or IP addresses

## Terraform State

Terraform state is excluded from Git. Early phases should use local state only while learning and validating. Remote state should be added later with an encrypted S3 backend, versioning, restricted IAM, and a documented migration checklist.

## AWS Credentials

Use one of these approaches locally:

- AWS CLI profile
- short-lived credentials
- IAM role when running on AWS infrastructure

Do not place credentials in Docker images, Terraform files, Python source, GitHub Actions secrets committed to the repo, or documentation examples.

## Logging

Logs should include enough context to debug service health and cloud operations, but must not include:

- credentials
- authorization headers
- full request headers
- private keys
- raw Terraform state
- personal email addresses

## Docker Socket

The health agent may eventually need container health information. If Docker socket access is used, mount it read-only and document the risk clearly. Docker socket access can effectively grant host-level control.

## Public Access

S3 buckets must block public access. Any future API Gateway route should start with cautious CORS defaults and avoid wildcard access unless there is a documented reason.
