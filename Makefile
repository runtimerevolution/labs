PROJECT_NAME = labs
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python

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
	ruff check --fix --select I
	ruff format

## Stops and removes all the services
.PHONY: down
down:
	$(shell cat .env.local | grep LOCAL_REPOSITORIES_PATH ) docker compose down

## Start all the services
.PHONY: up
up: down
	$(shell cat .env.local | grep LOCAL_REPOSITORIES_PATH ) docker compose up --build -d

## Start a python shell
.PHONY: shell
shell:
	ipython

## Run project tests
.PHONY: tests
tests:
	pytest ./labs

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
	DJANGO_SUPERUSER_PASSWORD=admin poetry run python labs/manage.py createsuperuser --noinput --username=admin --email=admin@example.com

loadfixtures:
	python labs/manage.py loaddata $(wildcard labs/fixtures/*.json)

setup: migrate loadfixtures createuser
