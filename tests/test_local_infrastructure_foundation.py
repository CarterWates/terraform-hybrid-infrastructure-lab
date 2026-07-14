import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LocalInfrastructureFoundationTests(unittest.TestCase):
    def test_docker_compose_defines_expected_services_and_ports(self):
        compose = ROOT / "local-infrastructure" / "docker-compose.yml"
        text = compose.read_text()

        for service in ("nginx", "prometheus", "grafana", "node-exporter"):
            self.assertIn(f"  {service}:", text)

        for port in ("8080:80", "9090:9090", "3000:3000", "9100:9100"):
            self.assertIn(port, text)

        self.assertIn("hybrid-lab", text)
        self.assertIn("healthcheck:", text)
        self.assertIn("curl -fsS http://localhost/", text)
        self.assertIn("grafana-data", text)
        self.assertIn("prometheus-data", text)

    def test_nginx_status_page_and_config_exist(self):
        index = ROOT / "local-infrastructure" / "nginx" / "index.html"
        config = ROOT / "local-infrastructure" / "nginx" / "nginx.conf"

        self.assertIn("Terraform-Managed Hybrid Infrastructure Lab", index.read_text())
        self.assertIn("listen 80", config.read_text())

    def test_prometheus_scrapes_local_stack(self):
        prometheus = ROOT / "local-infrastructure" / "prometheus" / "prometheus.yml"
        text = prometheus.read_text()

        self.assertIn("job_name: prometheus", text)
        self.assertIn("job_name: node-exporter", text)
        self.assertIn("prometheus:9090", text)
        self.assertIn("node-exporter:9100", text)

    def test_grafana_provisioning_and_dashboard_are_valid(self):
        datasource = (
            ROOT
            / "local-infrastructure"
            / "grafana"
            / "provisioning"
            / "datasources"
            / "prometheus.yml"
        )
        dashboard_provider = (
            ROOT
            / "local-infrastructure"
            / "grafana"
            / "provisioning"
            / "dashboards"
            / "dashboards.yml"
        )
        dashboard = (
            ROOT
            / "local-infrastructure"
            / "grafana"
            / "dashboards"
            / "host-overview.json"
        )

        self.assertIn("http://prometheus:9090", datasource.read_text())
        self.assertIn("/var/lib/grafana/dashboards", dashboard_provider.read_text())

        data = json.loads(dashboard.read_text())
        self.assertEqual(data["title"], "Hybrid Lab Host Overview")
        panel_titles = {panel["title"] for panel in data["panels"]}
        self.assertTrue({"CPU Usage", "Memory Usage", "Disk Usage", "System Uptime"}.issubset(panel_titles))

    def test_documentation_mentions_local_stack_commands(self):
        readme = (ROOT / "local-infrastructure" / "README.md").read_text()

        self.assertIn("docker compose config", readme)
        self.assertIn("docker compose up -d", readme)
        self.assertIn("macOS", readme)


if __name__ == "__main__":
    unittest.main()
