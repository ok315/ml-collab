@"
# Contributing Guide

## Branching Strategy

This project uses three permanent branches:

- `main` — production/release-ready code.
- `staging` — release-candidate integration and validation.
- `dev` — main development/integration branch.

Short-lived branches are used for individual tasks:

- `feat/<name>` — feature development.
- `data/<name>` — dataset/data changes.
- `exp/<member>-<idea>` — experiments and model tuning.
- `fix/<name>` — bug fixes.

The normal workflow is:

`feat/* / data/* / exp/* / fix/* -> dev -> staging -> main`

After the initial repository setup, contributors should not push directly to `dev`, `staging`, or `main`. Changes should be submitted through pull requests.

## Pull Request Workflow

1. Create a short-lived branch from the appropriate integration branch.
2. Make focused commits following the commit convention below.
3. Run the pre-commit checks locally.
4. Push the branch to GitHub.
5. Open a pull request targeting `dev`.
6. Request review from a teammate.
7. Address review feedback before merging.
8. Merge using squash merge.
9. Delete the short-lived branch after merging.

Changes are promoted from `dev` to `staging` and then from `staging` to `main` through reviewed pull requests.

## Commit Convention

Use Conventional Commit-style messages.

Examples:

- `feat: add customer churn model`
- `fix: handle missing values`
- `docs: update contribution guide`
- `test: add data quality tests`
- `chore: update project configuration`

Commits should be focused and describe the change clearly.

## Pre-commit

Install the configured pre-commit hooks with:

## Retrospective

During development, we encountered several issues that helped shape the team's workflow. Pre-commit initially exposed formatting and security-check problems, including Ruff changes and a false-positive high-entropy hash in `metrics.json`. We also had to update the detect-secrets baseline so that known non-secret hashes were handled consistently.

We standardized the repository around:
- pull requests for normal changes,
- teammate review before merging,
- Conventional Commit messages,
- squash merging,
- pre-commit checks for formatting, notebooks, large files, and secrets,
- DVC for dataset tracking,
- CI checks for linting, tests, data validation, and smoke training.

As a result, `CONTRIBUTING.md` documents the branch workflow, pull-request process, commit conventions, merge strategy, and pre-commit requirements so that contributors follow the same process instead of repeating the issues encountered during development.

```powershell
pre-commit install