# Grafana

Grafana is provisioned automatically when the Docker Compose stack starts.

Included provisioning:

- Prometheus data source at `http://prometheus:9090`
- `Hybrid Lab Host Overview` dashboard

The dashboard JSON is stored in `dashboards/host-overview.json`.
