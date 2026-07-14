# Docker Setup Runbook

The local monitoring stack requires Docker before `make docker-validate` or `make local-up` can run.

## macOS

Install Docker Desktop from Docker's official website, then start the Docker Desktop app once before using the CLI.

After installation, verify:

```bash
docker --version
docker compose version
```

If `docker` is still not found in a new terminal, open Docker Desktop and check that command line tools are installed or available on your shell `PATH`.

## Linux

Install Docker Engine and the Docker Compose plugin using your distribution's official package instructions.

After installation, verify:

```bash
docker --version
docker compose version
```

If Docker requires elevated privileges, either run Docker commands with the appropriate permissions or configure your user for Docker access using your distribution's recommended process.

## Project Checks

From the repository root:

```bash
make docker-validate
make local-up
make local-status
```

Expected local URLs after startup:

- Nginx: <http://localhost:8080>
- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000>
- Node Exporter metrics: <http://localhost:9100/metrics>

Stop the stack:

```bash
make local-down
```
