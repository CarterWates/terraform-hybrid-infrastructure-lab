# Phase 1 Repository Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first public-safe repository foundation for the Terraform-Managed Hybrid Infrastructure Lab.

**Architecture:** Create a documentation-first monorepo skeleton with explicit subsystem directories. Keep all implemented claims limited to repository structure and planning artifacts until later phases add working services.

**Tech Stack:** Markdown, Mermaid, Makefile, Git, GitHub.

## Global Constraints

- Do not commit credentials, `.env`, Terraform state, private keys, generated archives, or sensitive screenshots.
- Do not claim Docker, Terraform, Python agents, Lambda, or CI are implemented in this phase.
- Keep `.env.example` value-free.
- Do not run `terraform apply` or `terraform destroy` from this repository foundation.

---

### Task 1: Create Repository Skeleton

**Files:**
- Create: `README.md`
- Create: `.gitignore`
- Create: `.env.example`
- Create: `Makefile`
- Create: subsystem directories listed in the README

**Interfaces:**
- Produces: public repository shape for later phases

- [x] **Step 1: Initialize Git**

Run: `git init`
Expected: an empty Git repository exists at `.git/`.

- [x] **Step 2: Create directories**

Run: `mkdir -p local-infrastructure/nginx local-infrastructure/prometheus local-infrastructure/grafana/dashboards local-infrastructure/grafana/provisioning local-infrastructure/scripts agents/health-agent agents/backup-agent backend/health-api infrastructure/terraform/modules infrastructure/terraform/environments/dev tests docs/superpowers/specs docs/superpowers/plans docs/portfolio docs/runbooks .github/workflows`
Expected: all planned directories exist.

- [x] **Step 3: Add root foundation files**

Add `README.md`, `.gitignore`, `.env.example`, and `Makefile` with the public-safe content for this phase.

### Task 2: Add Supporting Documentation

**Files:**
- Create: `docs/ROADMAP.md`
- Create: `docs/SECURITY.md`
- Create: `docs/portfolio/SCREENSHOTS.md`
- Create: `docs/runbooks/TEARDOWN.md`

**Interfaces:**
- Consumes: root README project story
- Produces: phase roadmap, safety guidance, evidence checklist, and teardown guidance

- [x] **Step 1: Add roadmap**

Create `docs/ROADMAP.md` with the planned implementation phases from repository foundation through CI and release readiness.

- [x] **Step 2: Add security notes**

Create `docs/SECURITY.md` with rules for credentials, Terraform state, AWS authentication, logging, Docker socket access, and public access.

- [x] **Step 3: Add portfolio screenshot checklist**

Create `docs/portfolio/SCREENSHOTS.md` with planned screenshots and redaction rules.

- [x] **Step 4: Add teardown runbook**

Create `docs/runbooks/TEARDOWN.md` with local and Terraform teardown guidance.

### Task 3: Validate and Publish Readiness

**Files:**
- Read: all created files

**Interfaces:**
- Consumes: repository files
- Produces: local commit and remote-ready branch

- [ ] **Step 1: Verify file tree**

Run: `find . -path ./.git -prune -o -type f -print | sort`
Expected: only public-safe foundation files are present.

- [ ] **Step 2: Run Makefile checks**

Run: `make help`, `make tree`, and `make security-check`
Expected: commands exit successfully and do not expose secrets.

- [ ] **Step 3: Commit**

Run: `git add .` and `git commit -m "Initialize hybrid infrastructure lab"`
Expected: one local commit contains the foundation files.

- [ ] **Step 4: Configure GitHub remote**

Run: `git remote add origin https://github.com/CarterWates/terraform-hybrid-infrastructure-lab.git`
Expected: `origin` points to the intended GitHub repository.

- [ ] **Step 5: Push**

Run: `git push -u origin main`
Expected: push succeeds if GitHub authentication is valid. If authentication is invalid, leave the local repository committed and ready for `gh auth login -h github.com`.
