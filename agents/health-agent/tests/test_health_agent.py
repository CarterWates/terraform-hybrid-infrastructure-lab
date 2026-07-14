import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))


class ConfigTests(unittest.TestCase):
    def test_config_uses_environment_values_and_defaults(self):
        from health_agent.config import AgentConfig

        env = {
            "NODE_ID": "homelab-node-001",
            "HEALTH_INTERVAL_SECONDS": "45",
            "DOCKER_TIMEOUT_SECONDS": "3",
        }

        config = AgentConfig.from_env(env)

        self.assertEqual(config.node_id, "homelab-node-001")
        self.assertEqual(config.interval_seconds, 45)
        self.assertEqual(config.docker_timeout_seconds, 3)
        self.assertEqual(config.agent_version, "1.0.0")

    def test_config_defaults_node_id_when_missing(self):
        from health_agent.config import AgentConfig

        config = AgentConfig.from_env({})

        self.assertEqual(config.node_id, "homelab-node-001")
        self.assertEqual(config.interval_seconds, 60)


class PayloadTests(unittest.TestCase):
    def test_build_payload_includes_metrics_services_and_version(self):
        from health_agent.config import AgentConfig
        from health_agent.payload import build_payload

        config = AgentConfig(node_id="node-1", interval_seconds=60, docker_timeout_seconds=2)
        metrics = {
            "hostname": "lab-host",
            "cpuPercent": 12.5,
            "memoryPercent": 40.0,
            "diskPercent": 55.1,
            "uptimeSeconds": 1234,
        }
        services = {"nginx": "healthy", "prometheus": "healthy", "grafana": "unhealthy"}

        payload = build_payload(config, metrics, services, timestamp="2026-07-14T16:00:00Z")

        self.assertEqual(payload["nodeId"], "node-1")
        self.assertEqual(payload["timestamp"], "2026-07-14T16:00:00Z")
        self.assertEqual(payload["hostname"], "lab-host")
        self.assertEqual(payload["cpuPercent"], 12.5)
        self.assertEqual(payload["services"]["grafana"], "unhealthy")
        self.assertEqual(payload["agentVersion"], "1.0.0")

    def test_collect_metrics_survives_individual_metric_failure(self):
        from health_agent import metrics

        with mock.patch.object(metrics, "_cpu_percent", side_effect=RuntimeError("cpu failed")):
            result = metrics.collect_system_metrics()

        self.assertEqual(result["cpuPercent"], None)
        self.assertIn("hostname", result)
        self.assertIn("memoryPercent", result)
        self.assertIn("diskPercent", result)
        self.assertIn("uptimeSeconds", result)


class DockerServiceTests(unittest.TestCase):
    def test_check_services_marks_docker_unavailable(self):
        from health_agent.docker_health import check_services

        with mock.patch("subprocess.run", side_effect=FileNotFoundError("docker")):
            result = check_services(["nginx", "prometheus"], timeout_seconds=1)

        self.assertEqual(result, {"nginx": "docker_unavailable", "prometheus": "docker_unavailable"})

    def test_check_services_reads_container_health_status(self):
        from health_agent.docker_health import check_services

        completed = subprocess.CompletedProcess(
            args=["docker"],
            returncode=0,
            stdout="hybrid-lab-nginx:healthy\nhybrid-lab-prometheus:running\n",
            stderr="",
        )

        with mock.patch("subprocess.run", return_value=completed):
            result = check_services(["nginx", "prometheus", "grafana"], timeout_seconds=1)

        self.assertEqual(result["nginx"], "healthy")
        self.assertEqual(result["prometheus"], "running")
        self.assertEqual(result["grafana"], "not_found")


class CliTests(unittest.TestCase):
    def test_once_mode_prints_single_json_payload(self):
        from health_agent import cli

        with mock.patch.dict(os.environ, {"NODE_ID": "cli-node"}, clear=True):
            with mock.patch(
                "health_agent.cli.collect_system_metrics",
                return_value={
                    "hostname": "cli-host",
                    "cpuPercent": 1.0,
                    "memoryPercent": 2.0,
                    "diskPercent": 3.0,
                    "uptimeSeconds": 4,
                },
            ):
                with mock.patch(
                    "health_agent.cli.check_services",
                    return_value={"nginx": "healthy", "prometheus": "healthy", "grafana": "healthy"},
                ):
                    output = io.StringIO()
                    with redirect_stdout(output):
                        exit_code = cli.main(["--once"])

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["nodeId"], "cli-node")
        self.assertEqual(payload["hostname"], "cli-host")
        self.assertEqual(payload["services"]["nginx"], "healthy")


if __name__ == "__main__":
    unittest.main()
