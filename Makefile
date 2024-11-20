PROJECT_NAME = labs
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python
ENV ?= local
ENV_FILE := .env.$(ENV)

include $(ENV_FILE)
export
#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint and format using ruff
.PHONY: lint
lint:
	ruff lint --fix --select I
	ruff format

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml labs

## Stops and removes all the services
.PHONY: down
down:
	docker compose --env-file=$(ENV_FILE) down

## Start all the services
.PHONY: up
up: down
	docker compose --env-file=$(ENV_FILE) up --build -d

.PHONY: simple
simple: down
	docker compose --env-file=$(ENV_FILE) up labs-db -d

## Start a python shell
.PHONY: shell
shell:
	ipython

## Run project tests
.PHONY: tests
tests:
	pytest ./labs

.PHONY: clean_tests
clean_tests:
	@if [ ! -d ./labs/test/vcr_cassettes ]; then \
		echo "labs/test/vcr_cassettes does not exist"; \
	else \
		rm -rf labs/test/vcr_cassettes; \
	fi

## Pull given model from ollama (use `make ollama model=<model name>`)
.PHONY: ollama
ollama:
	docker compose exec ollama ollama pull $(model)


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)

runserver:
	poetry run python labs/manage.py runserver

migrations:
	poetry run python labs/manage.py makemigrations

migrate:
	poetry run python labs/manage.py migrate

createuser:
	DJANGO_SUPERUSER_PASSWORD=admin poetry run python labs/manage.py createsuperuser --noinput --username=admin --email=a@b.com

load_fixtures:
	python labs/manage.py loaddata $(wildcard labs/fixtures/*.json)
