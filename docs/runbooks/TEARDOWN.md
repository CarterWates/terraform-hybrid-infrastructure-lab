# Teardown Runbook

This runbook will become executable once the AWS and Docker phases are implemented.

## Local Services

Planned command:

```bash
cd local-infrastructure
docker compose down
```

Volumes should be removed only when data loss is intentional and documented.

## AWS Resources

Terraform-managed resources should be destroyed from the matching environment directory:

```bash
cd infrastructure/terraform/environments/dev
terraform plan -destroy
terraform destroy
```

Review the destroy plan before approving it. Confirm that no shared or manually created resources are included.

## Manual Checks

After teardown, confirm:

- no unexpected S3 buckets remain
- DynamoDB tables created by this lab are gone
- Lambda functions and API Gateway routes are gone
- CloudWatch log groups are removed or intentionally retained
- SNS topics and subscriptions are removed
