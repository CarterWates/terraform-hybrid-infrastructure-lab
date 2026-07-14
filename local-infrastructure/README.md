# Local Infrastructure

This directory contains the local Docker Compose monitoring stack for the lab.

## Services

| Service | URL | Purpose |
| --- | --- | --- |
| Nginx | <http://localhost:8080> | Demo infrastructure status page |
| Prometheus | <http://localhost:9090> | Metrics collection |
| Grafana | <http://localhost:3000> | Metrics dashboards |
| Node Exporter | <http://localhost:9100/metrics> | Host metrics exporter |

## Setup

From the repository root, create a local environment file:

```bash
cp .env.example .env
```

Set `GRAFANA_ADMIN_PASSWORD` before starting Grafana.

## Validate

```bash
cd local-infrastructure
docker compose config
```

## Start

```bash
cd local-infrastructure
docker compose up -d
docker compose ps
```

## Stop

```bash
cd local-infrastructure
docker compose down
```

Add `--volumes` only when you intentionally want to remove persisted Prometheus and Grafana data.

## Platform Notes

The default Node Exporter configuration is portable across Docker Desktop and Linux Docker Engine. It does not mount `/proc`, `/sys`, the Docker socket, or the host root filesystem.

On macOS with Docker Desktop, containers run inside a lightweight Linux VM. Node Exporter metrics may describe that VM more than the physical Mac host. This is expected for a local portfolio lab and should be documented in screenshots or write-ups.

On Linux, a later override file can add read-only host mounts for deeper host metrics after the base stack is stable.

## Security Notes

- Grafana reads the admin password from an environment variable.
- No credentials are stored in this directory.
- Containers are not privileged.
- The stack exposes ports only on the local development machine by default.
- Docker socket access is not used in this phase.
