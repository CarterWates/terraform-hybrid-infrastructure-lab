# Phase 1 Repository Foundation Design

## Goal

Create a public-safe, portfolio-ready foundation for the Terraform-Managed Hybrid Infrastructure Lab without claiming unimplemented services are complete.

## Scope

This phase creates structure, documentation, and guardrails only. Docker services, Python agents, Terraform resources, Lambda functions, and full CI validation are planned future work.

## Architecture

The repository is organized as a monorepo with clear subsystem boundaries:

- `local-infrastructure/` for Docker Compose, Nginx, Prometheus, Grafana, and helper scripts.
- `agents/` for local Python agents.
- `backend/` for cloud-side application code.
- `infrastructure/terraform/` for Terraform modules and environments.
- `docs/` for architecture, roadmap, runbooks, portfolio evidence, and planning artifacts.
- `.github/workflows/` for CI workflows.

## Documentation

The root README presents the project purpose, planned architecture, technology stack, repository structure, current status, and security principles. Supporting docs hold the roadmap, security notes, screenshot checklist, and teardown runbook.

## Safety Controls

The first version excludes secrets, Terraform state, virtual environments, generated backups, local logs, and private screenshot material. `.env.example` contains variable names only.

## Validation

The initial repo can be validated with:

- `make help`
- `make repo-check`
- `make tree`
- `make security-check`
- `git status --short`

## Publishing

The repository should be committed locally and connected to `CarterWates/terraform-hybrid-infrastructure-lab.git`. If GitHub CLI authentication is invalid, the local commit should still be left ready to push after re-authentication.
