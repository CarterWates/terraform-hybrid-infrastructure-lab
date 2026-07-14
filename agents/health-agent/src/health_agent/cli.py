"""Command-line entry point for the local health agent."""

from __future__ import annotations

import argparse
import json
import logging
import time

from health_agent.config import AgentConfig
from health_agent.docker_health import check_services
from health_agent.metrics import collect_system_metrics
from health_agent.payload import build_payload


SERVICES = ["nginx", "prometheus", "grafana"]


def main(argv: list[str] | None = None) -> int:
    """Run the health agent once or on an interval."""

    parser = argparse.ArgumentParser(description="Collect local hybrid lab health data.")
    parser.add_argument("--once", action="store_true", help="Print one health payload and exit.")
    parser.add_argument("--verbose", action="store_true", help="Enable info-level logs.")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    config = AgentConfig.from_env()

    if args.once:
        print(json.dumps(_collect_payload(config), sort_keys=True))
        return 0

    while True:
        print(json.dumps(_collect_payload(config), sort_keys=True), flush=True)
        time.sleep(config.interval_seconds)


def _collect_payload(config: AgentConfig) -> dict[str, object]:
    metrics = collect_system_metrics()
    services = check_services(SERVICES, config.docker_timeout_seconds)
    return build_payload(config, metrics, services)
