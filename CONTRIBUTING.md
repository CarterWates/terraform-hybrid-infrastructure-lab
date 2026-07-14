# Contributing

This is a personal portfolio lab, but the repository is organized so changes can be reviewed cleanly.

## Development Rules

- Work one phase at a time.
- Do not commit credentials or local environment files.
- Validate each phase before committing.
- Keep documentation aligned with what the code actually does.
- Prefer small, reviewable commits.

## Commit Style

Use short, descriptive commit messages:

```text
Add local Docker monitoring stack
Provision Grafana dashboards automatically
Add local Python health agent
```

## Validation

Run the relevant checks before opening a pull request. During the foundation phase:

```bash
make help
make tree
make security-check
```

Later phases will add Terraform, Docker, Python, and CI validation.
