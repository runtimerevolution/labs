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

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 labs
	isort --check --diff --profile black labs
	black --check --config pyproject.toml labs

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml labs

## Set up project
.PHONY: setup
setup:
	$(PYTHON_INTERPRETER) labs/setup.py

.PHONY: tests
tests:
	pytest

.PHONY: clean_tests
clean_tests:
	@if [ ! -d ./labs/test/vcr_cassettes ]; then \
		echo "labs/test/vcr_cassettes does not exist"; \
	else \
		rm -rf labs/test/vcr_cassettes; \
	fi

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

api:
	fastapi dev labs/api/main.py  
