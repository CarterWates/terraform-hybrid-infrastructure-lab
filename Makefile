.PHONY: help repo-check tree security-check local-up local-down local-logs local-status docker-validate test-health-agent test-backup-agent test-health-api test-all terraform-fmt terraform-validate terraform-plan lint clean

help:
	@echo "Terraform-Managed Hybrid Infrastructure Lab"
	@echo ""
	@echo "Foundation commands:"
	@echo "  make repo-check        Show git status and tracked files"
	@echo "  make tree              Show the repository file tree"
	@echo "  make security-check    Search for common secret and state file patterns"
	@echo ""
	@echo "Future implementation commands:"
	@echo "  make local-up          Start local Docker services"
	@echo "  make local-down        Stop local Docker services"
	@echo "  make local-logs        Tail local Docker logs"
	@echo "  make local-status      Show local Docker service status"
	@echo "  make docker-validate   Validate Docker Compose configuration"
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
	@test ! -f .env || (echo ".env exists locally and must remain untracked"; exit 1)
	@find . -path ./.git -prune -o \( -name "*.tfstate" -o -name "*.tfvars" -o -name "*.pem" -o -name "*.key" \) -print

local-up:
	@echo "Not implemented yet. This target will start local-infrastructure/docker-compose.yml."

local-down:
	@echo "Not implemented yet. This target will stop local-infrastructure/docker-compose.yml."

local-logs:
	@echo "Not implemented yet. This target will tail local Docker logs."

local-status:
	@echo "Not implemented yet. This target will show local Docker service status."

docker-validate:
	@echo "Not implemented yet. Docker Compose configuration will be added in a later phase."

test-health-agent:
	@echo "Not implemented yet. Health agent tests will be added in a later phase."

test-backup-agent:
	@echo "Not implemented yet. Backup agent tests will be added in a later phase."

test-health-api:
	@echo "Not implemented yet. Health API tests will be added in a later phase."

test-all:
	@echo "Not implemented yet. Test commands will be wired in as subsystems are implemented."

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
