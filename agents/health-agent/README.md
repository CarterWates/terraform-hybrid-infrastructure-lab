# Health Agent

Python agent for local health reporting.

The current version collects best-effort local metrics, checks expected Docker service health when Docker is available, and prints one JSON payload locally. AWS delivery will be added after the serverless ingestion API exists.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `NODE_ID` | `homelab-node-001` | Logical node identifier |
| `HEALTH_INTERVAL_SECONDS` | `60` | Loop interval for continuous mode |
| `DOCKER_TIMEOUT_SECONDS` | `2` | Timeout for Docker CLI health checks |

## Run Once

From this directory:

```bash
PYTHONPATH=src python3 -m health_agent --once
```

If Docker is not installed, service statuses are reported as `docker_unavailable` instead of crashing.

## Loop Mode

```bash
PYTHONPATH=src python3 -m health_agent
```

Stop with `Ctrl+C`.

## Tests

From the repository root:

```bash
python3 -m unittest discover -s agents/health-agent/tests
```
