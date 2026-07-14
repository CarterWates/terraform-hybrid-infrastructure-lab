resource "aws_dynamodb_table" "health" {
  name         = var.health_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "nodeId"
  range_key    = "timestamp"

  attribute {
    name = "nodeId"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  ttl {
    attribute_name = var.health_ttl_attribute
    enabled        = var.enable_health_ttl
  }

  tags = {
    Name = var.health_table_name
  }
}

resource "aws_s3_bucket" "backups" {
  bucket        = var.backup_bucket_name
  force_destroy = var.backup_bucket_force_destroy

  tags = {
    Name = var.backup_bucket_name
  }
}

resource "aws_s3_bucket_public_access_block" "backups" {
  bucket = aws_s3_bucket.backups.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    id     = "backup-retention"
    status = "Enabled"

    filter {
      prefix = ""
    }

    noncurrent_version_expiration {
      noncurrent_days = var.backup_lifecycle_expiration_days
    }

    expiration {
      days = var.backup_lifecycle_expiration_days
    }

    transition {
      days          = var.backup_lifecycle_transition_days
      storage_class = "STANDARD_IA"
    }
  }
}

resource "aws_sns_topic" "alerts" {
  name = "${local.name_prefix}-alerts"
}

resource "aws_sns_topic_subscription" "email_alerts" {
  count = var.alert_email == "" ? 0 : 1

  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

resource "aws_cloudwatch_log_group" "health_api" {
  name              = "/aws/lambda/hybrid-lab-health-api"
  retention_in_days = var.log_retention_days
}

resource "aws_cloudwatch_log_group" "monitoring_jobs" {
  name              = "/hybrid-lab/monitoring-jobs"
  retention_in_days = var.log_retention_days
}
