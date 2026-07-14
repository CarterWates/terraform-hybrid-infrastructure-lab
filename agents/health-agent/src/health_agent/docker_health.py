"""Docker service health checks for the local monitoring stack."""

from __future__ import annotations

import subprocess


CONTAINER_PREFIX = "hybrid-lab-"


def check_services(service_names: list[str], timeout_seconds: int) -> dict[str, str]:
    """Return a health status for each expected Docker Compose service."""

    try:
        completed = subprocess.run(
            [
                "docker",
                "ps",
                "--format",
                "{{.Names}}:{{if .Status}}{{.Status}}{{end}}",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError:
        return {service: "docker_unavailable" for service in service_names}
    except subprocess.TimeoutExpired:
        return {service: "docker_timeout" for service in service_names}

    if completed.returncode != 0:
        return {service: "docker_error" for service in service_names}

    observed = _parse_docker_ps(completed.stdout)
    return {service: observed.get(f"{CONTAINER_PREFIX}{service}", "not_found") for service in service_names}


def _parse_docker_ps(output: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for line in output.splitlines():
        if ":" not in line:
            continue
        name, status = line.split(":", 1)
        statuses[name] = _normalize_status(status)
    return statuses


def _normalize_status(status: str) -> str:
    lowered = status.lower()
    if "(healthy)" in lowered or lowered == "healthy":
        return "healthy"
    if "(unhealthy)" in lowered or lowered == "unhealthy":
        return "unhealthy"
    if "up " in lowered or lowered == "running":
        return "running"
    if "exited" in lowered:
        return "stopped"
    return status.strip() or "unknown"
