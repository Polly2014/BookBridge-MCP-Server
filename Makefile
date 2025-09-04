# Makefile for BookBridge-MCP
# Requires Poetry to be installed

.PHONY: help install dev-install test lint format type-check clean build run client-example setup

help: ## Show this help message
	@echo "BookBridge-MCP Development Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Set up the project with Poetry
	python setup_poetry.py

install: ## Install dependencies
	poetry install

dev-install: ## Install with development dependencies
	poetry install --with dev --with client

test: ## Run tests
	poetry run pytest -v

test-coverage: ## Run tests with coverage report
	poetry run pytest --cov=src --cov-report=html --cov-report=term

lint: ## Run linting (flake8)
	poetry run flake8 src/ tests/ examples/

format: ## Format code (black + isort)
	poetry run black .
	poetry run isort .

format-check: ## Check code formatting without making changes
	poetry run black --check .
	poetry run isort --check-only .

type-check: ## Run type checking (mypy)
	poetry run mypy src/

pre-commit: ## Run pre-commit hooks on all files
	poetry run pre-commit run --all-files

clean: ## Clean up temporary files and caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -name ".coverage" -delete
	find . -name "htmlcov" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +

build: ## Build the package
	poetry build

run: ## Start the MCP server
	poetry run python start.py

server: ## Start the MCP server (alias for run)
	poetry run python start.py

client-example: ## Run the client example
	poetry run python examples/client_example.py

shell: ## Activate Poetry shell
	poetry shell

env-info: ## Show environment information
	poetry env info

show-deps: ## Show installed dependencies
	poetry show

update-deps: ## Update dependencies
	poetry update

add-dep: ## Add a new dependency (usage: make add-dep PACKAGE=package_name)
	poetry add $(PACKAGE)

add-dev-dep: ## Add a new development dependency (usage: make add-dev-dep PACKAGE=package_name)
	poetry add --group dev $(PACKAGE)

install-git-hooks: ## Install git hooks
	poetry run pre-commit install

check: format-check lint type-check test ## Run all checks (format, lint, type-check, test)

ci: format-check lint type-check test-coverage ## Run CI pipeline

# Development workflow shortcuts
dev-setup: dev-install install-git-hooks ## Complete development setup
	@echo "✅ Development environment ready!"
	@echo "Next steps:"
	@echo "  1. Run 'make run' to start the server"
	@echo "  2. Run 'make client-example' to test the client"
	@echo "  3. Run 'make test' to run tests"

quick-test: ## Quick test without coverage
	poetry run pytest tests/ -x -v

watch-test: ## Run tests in watch mode (requires pytest-xvfb)
	poetry run ptw tests/
