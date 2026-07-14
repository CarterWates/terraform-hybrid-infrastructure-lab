output "health_table_name" {
  description = "DynamoDB table name used for health reports."
  value       = aws_dynamodb_table.health.name
}

output "health_table_arn" {
  description = "DynamoDB table ARN used for later Lambda IAM permissions."
  value       = aws_dynamodb_table.health.arn
}

output "backup_bucket_name" {
  description = "S3 bucket name used for configuration backups."
  value       = aws_s3_bucket.backups.bucket
}

output "backup_bucket_arn" {
  description = "S3 bucket ARN used for later backup-agent IAM permissions."
  value       = aws_s3_bucket.backups.arn
}

output "alerts_topic_arn" {
  description = "SNS topic ARN for infrastructure and outage alerts."
  value       = aws_sns_topic.alerts.arn
}

output "health_api_log_group_name" {
  description = "CloudWatch log group reserved for the future health API Lambda."
  value       = aws_cloudwatch_log_group.health_api.name
}

output "monitoring_jobs_log_group_name" {
  description = "CloudWatch log group reserved for monitoring jobs."
  value       = aws_cloudwatch_log_group.monitoring_jobs.name
}
