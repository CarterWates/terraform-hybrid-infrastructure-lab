"""Configuration loading for the health agent."""

from __future__ import annotations

from dataclasses import dataclass
from os import environ
from typing import Mapping

from health_agent import __version__


@dataclass(frozen=True)
class AgentConfig:
    """Runtime configuration for local health collection."""

    node_id: str = "homelab-node-001"
    interval_seconds: int = 60
    docker_timeout_seconds: int = 2
    agent_version: str = __version__

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "AgentConfig":
        """Build configuration from environment variables."""

        values = environ if env is None else env
        return cls(
            node_id=values.get("NODE_ID", "homelab-node-001") or "homelab-node-001",
            interval_seconds=_positive_int(values.get("HEALTH_INTERVAL_SECONDS"), 60),
            docker_timeout_seconds=_positive_int(values.get("DOCKER_TIMEOUT_SECONDS"), 2),
        )


def _positive_int(value: str | None, default: int) -> int:
    if value is None or value == "":
        return default

    try:
        parsed = int(value)
    except ValueError:
        return default

    return parsed if parsed > 0 else default
