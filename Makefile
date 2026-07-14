.PHONY: help repo-check tree security-check check-docker local-up local-down local-logs local-status docker-validate test-health-agent test-backup-agent test-health-api test-all terraform-fmt terraform-validate terraform-plan lint clean

help:
	@echo "Terraform-Managed Hybrid Infrastructure Lab"
	@echo ""
	@echo "Foundation commands:"
	@echo "  make repo-check        Show git status and tracked files"
	@echo "  make tree              Show the repository file tree"
	@echo "  make security-check    Search for common secret and state file patterns"
	@echo ""
	@echo "Local Docker commands:"
	@echo "  make local-up          Start local Docker services"
	@echo "  make local-down        Stop local Docker services"
	@echo "  make local-logs        Tail local Docker logs"
	@echo "  make local-status      Show local Docker service status"
	@echo "  make docker-validate   Validate Docker Compose configuration"
	@echo ""
	@echo "Validation commands:"
	@echo "  make test-all          Run all implemented tests"
	@echo "  make terraform-validate Validate Terraform once implemented"
	@echo ""
	@echo "Safety note: this Makefile will not run terraform apply or destroy."

repo-check:
	git status --short
	git ls-files

tree:
	find . -path ./.git -prune -o -type f -print | sort

security-check:
	@echo "Checking for files that should not be committed..."
	@! git ls-files --error-unmatch .env >/dev/null 2>&1 || (echo ".env is tracked and must be removed from Git"; exit 1)
	@find . -path ./.git -prune -o \( -name "*.tfstate" -o -name "*.tfvars" -o -name "*.pem" -o -name "*.key" \) -print

check-docker:
	@command -v docker >/dev/null 2>&1 || (echo "Docker is required for this command. Install Docker Desktop or Docker Engine, then retry."; exit 127)

local-up: check-docker
	cd local-infrastructure && docker compose --env-file ../.env up -d

local-down: check-docker
	cd local-infrastructure && docker compose --env-file ../.env down

local-logs: check-docker
	cd local-infrastructure && docker compose --env-file ../.env logs -f

local-status: check-docker
	cd local-infrastructure && docker compose --env-file ../.env ps

docker-validate: check-docker
	cd local-infrastructure && docker compose --env-file ../.env config

test-health-agent:
	python3 -m unittest discover -s agents/health-agent/tests

test-backup-agent:
	@echo "Not implemented yet. Backup agent tests will be added in a later phase."

test-health-api:
	@echo "Not implemented yet. Health API tests will be added in a later phase."

test-all:
	python3 -m unittest discover -s tests
	python3 -m unittest discover -s agents/health-agent/tests

terraform-fmt:
	@echo "Not implemented yet. Terraform files will be added in a later phase."

terraform-validate:
	@echo "Not implemented yet. Terraform files will be added in a later phase."

terraform-plan:
	@echo "Not implemented yet. This target will run terraform plan only, never apply."

lint:
	@echo "Not implemented yet. Linting will be configured with the Python projects."

clean:
	@echo "This placeholder does not remove files yet. Destructive cleanup will be explicit when implemented."
