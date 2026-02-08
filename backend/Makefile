# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
.DEFAULT_GOAL := help
SHELL         := /bin/bash

# Project metadata
PROJECT_NAME := LLMToolsetBackendServer
VERSION      := $(shell git describe --tags --always --dirty 2>/dev/null || echo "v0.1.0")
COMMIT_HASH  := $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_TIME   := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

# Python variables
PYTHON_FILES      := $(shell find . -type f -name '*.py' \
	-not -path "./venv/*" \
	-not -path "./.venv/*" \
)
PYTHON_TEST_FILES := $(shell find . -type f -name '*_test.py' \
	-not -path "./venv/*" \
	-not -path "./.venv/*" \
)
CURR_DIR          := $(shell pwd)

# =============================================================================
# TARGETS
# =============================================================================

.PHONY: help
help:  ## Display this help screen
	@echo "$(PROJECT_NAME)"
	@echo "Current Version: $(VERSION) ($(COMMIT_HASH))"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Code Quality

.PHONY: fmt
fmt: ## Format code
	@echo "Formatting code..."
	@uv run ruff format $(PYTHON_FILES)

.PHONY: lint
lint: ## Run linters and fix issues
	@echo "Running linters..."
	@uv run ruff check --fix $(PYTHON_FILES)

.PHONY: all
all: clean lint fmt test ## Clean, lint, format, and test

##@ Server

.PHONY: dev
dev: ## Run development server with auto-reload
	@echo "Starting development server..."
	@uv run flask run --host=0.0.0.0 --port=15050 --reload

.PHONY: run
run: ## Run production server with uwsgi
	@echo "Starting production server..."
	@export REPO_ROOT_PATH=$(CURR_DIR) && uv run uwsgi --ini uwsgi.ini

.PHONY: stop
stop: ## Stop the uwsgi server
	@echo "Stopping server..."
	@uv run uwsgi --stop $(PROJECT_NAME).pid

##@ Testing

.PHONY: test
test: ## Run unit tests with pytest
	@echo "Running unit tests..."
	@(export PYTHONPATH=${PYTHONPATH}:${CURR_DIR} && \
		uv run pytest -vv $(PYTHON_TEST_FILES))

##@ Cleanup

.PHONY: clean
clean: ## Clean temporary files and caches
	@echo "Cleaning..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
