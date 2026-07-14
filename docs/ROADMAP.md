# Implementation Roadmap

This roadmap keeps the lab honest and incremental. Each phase should end with validation and a commit.

## Phase 1: Repository Foundation

- Create the project structure.
- Add documentation and safety guardrails.
- Add `.gitignore`, `.env.example`, and placeholder developer commands.
- Publish the initial public-safe repository.

## Phase 2: Local Docker Monitoring Stack

- Add Nginx, Prometheus, Grafana, and Node Exporter.
- Use stable image tags, a dedicated Docker network, named volumes, and healthchecks.
- Document macOS and Linux differences for host metrics.
- Validate with `docker compose config` and `docker compose up -d`.

## Phase 3: Grafana Provisioning

- Provision Prometheus as the default data source.
- Add a host metrics dashboard for CPU, memory, disk, network, and uptime.
- Store dashboard JSON and provisioning YAML in the repository.

## Phase 4: Python Health Agent

- Collect node identity, timestamp, host metrics, service health, and agent version.
- Print JSON locally before any AWS integration.
- Add `--once`, loop mode, environment configuration, structured logging, and pytest coverage.

Status: initial local JSON output and unit tests are implemented. AWS delivery is intentionally deferred until the ingestion API exists.

## Phase 5: Terraform AWS Foundation

- Provision DynamoDB, S3, CloudWatch log groups, SNS, and least-privilege IAM where needed.
- Keep names configurable and state out of Git.
- Validate with `terraform fmt`, `terraform validate`, and reviewed `terraform plan`.

Status: dev environment foundation files are implemented. Running `terraform init` and `terraform validate` requires Terraform and AWS provider download access.

## Phase 6: Lambda Health API

- Accept `POST /health` telemetry through API Gateway.
- Validate payloads and store accepted reports in DynamoDB.
- Add structured logs and tests.

## Phase 7: Agent-to-AWS Integration

- Send health payloads to the deployed API endpoint.
- Add bounded retries, timeouts, request IDs, and optional failed-payload spooling.

## Phase 8: Backup Agent

- Archive allowlisted non-secret project configuration.
- Upload encrypted backups to the Terraform-managed S3 bucket.
- Exclude credentials, Terraform state, private keys, and generated build artifacts.

## Phase 9: Alerts and Outage Detection

- Add CloudWatch alarms for Lambda, API Gateway, and DynamoDB.
- Add missing-heartbeat detection with scheduled Lambda execution.
- Send alerts and recovery notifications through SNS.

## Phase 10: CI and Release Readiness

- Add GitHub Actions for Terraform formatting and validation, Python tests, Docker validation, and secret scanning.
- Run a security-focused review before public release.
- Capture portfolio screenshots with sensitive values redacted.

## Version Two Ideas

These are intentionally out of scope until the MVP is complete:

- Kubernetes
- multiple local nodes
- Raspberry Pi or EC2 nodes
- authentication
- OpenTelemetry
- Loki
- Alertmanager
- GitHub OIDC deployments
- dev and production Terraform environments
- Ansible host configuration
- cost dashboards
- chaos testing
