# Screenshot Checklist

Add screenshots only after each phase is actually implemented and running.

## Planned Evidence

- Docker Compose services running
- Nginx status page
- Prometheus targets
- Grafana dashboard
- Health agent local JSON output
- API Gateway route
- Lambda logs
- DynamoDB health records
- S3 backup objects
- CloudWatch alarm
- SNS alert email
- Terraform plan
- GitHub Actions passing workflow

## Redaction Rules

Before committing screenshots, remove:

- AWS account IDs
- access keys or tokens
- personal email addresses
- private IP addresses if sensitive
- bucket names if sensitive
- API Gateway URLs if not intended for public sharing
- Terraform state contents
