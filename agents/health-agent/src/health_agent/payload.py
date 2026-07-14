"""JSON payload construction for health reports."""

from __future__ import annotations

from typing import Any

from health_agent.config import AgentConfig
from health_agent.metrics import utc_timestamp


def build_payload(
    config: AgentConfig,
    metrics: dict[str, Any],
    services: dict[str, str],
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Combine config, metrics, and service health into one report."""

    return {
        "nodeId": config.node_id,
        "timestamp": timestamp or utc_timestamp(),
        "hostname": metrics.get("hostname"),
        "cpuPercent": metrics.get("cpuPercent"),
        "memoryPercent": metrics.get("memoryPercent"),
        "diskPercent": metrics.get("diskPercent"),
        "uptimeSeconds": metrics.get("uptimeSeconds"),
        "services": services,
        "agentVersion": config.agent_version,
    }
