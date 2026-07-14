# Architecture

The final lab will connect local infrastructure telemetry to AWS-managed storage, logging, alerting, and backups.

## Local Layer

The local layer is planned as a Docker Compose stack:

- Nginx serves a small status page.
- Prometheus collects local metrics.
- Grafana visualizes metrics from Prometheus.
- Node Exporter exposes host metrics where supported.
- The health agent collects system and service state.
- The backup agent archives approved configuration files.

## Cloud Layer

The AWS layer will be provisioned with Terraform:

- API Gateway exposes a `POST /health` endpoint.
- Lambda validates telemetry payloads.
- DynamoDB stores health reports.
- S3 stores encrypted configuration backups.
- CloudWatch stores logs and powers alarms.
- SNS sends outage and recovery notifications.
- IAM roles and policies keep permissions scoped.

## Telemetry Flow

```mermaid
sequenceDiagram
    participant Agent as Local Health Agent
    participant API as API Gateway
    participant Lambda as Lambda Health API
    participant DDB as DynamoDB
    participant CW as CloudWatch
    participant SNS as SNS

    Agent->>Agent: Collect host and service metrics
    Agent->>API: POST /health
    API->>Lambda: Invoke handler
    Lambda->>Lambda: Validate payload
    Lambda->>DDB: Store report
    Lambda->>CW: Emit structured logs
    CW->>SNS: Trigger alerts when thresholds fail
```

## Backup Flow

```mermaid
flowchart LR
    ALLOWLIST[Allowlisted config paths]
    ARCHIVE[Timestamped tar.gz archive]
    HASH[SHA-256 checksum]
    S3[(Encrypted S3 bucket)]

    ALLOWLIST --> ARCHIVE
    ARCHIVE --> HASH
    HASH --> S3
```

## Design Boundaries

- Local code should run without AWS until cloud integration is explicitly enabled.
- Terraform should not depend on local Docker state.
- Python agents should read configuration from environment variables.
- Cloud resources should be small, configurable, and easy to destroy.
- Documentation should distinguish implemented behavior from planned behavior.
