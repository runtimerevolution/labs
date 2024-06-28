#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = labs
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Start working on the project
.PHONY: start
start:
	@if brew ls --versions curl; then \
		brew upgrade curl; \
	else \
		brew install curl; \
	fi
	@if curl -fsSL https://pixi.sh/install.sh | bash; then \
		export "Pixi installed in the first attempt."; \
	else \
		echo "First Pixi installation attempt failed."; \
		echo "Running brew to install pixi..."; \
		export PIXI_INSTALLATION=False; \
		brew install pixi; \
	fi
	@if [ ! -f ./pixi.lock ]; then \
		echo "pixi.lock does not exist"; \
	else \
		rm pixi.lock; \
	fi
	pixi install


## Install Python Dependencies
.PHONY: requirements
requirements:
	conda env update --name $(PROJECT_NAME) --file environment.yml --prune


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


## Download Data from storage system
.PHONY: sync_data_down
sync_data_down:
	aws s3 sync s3://bucket-name/data/\
		data/ 
	

## Upload Data to storage system
.PHONY: sync_data_up
sync_data_up:
	aws s3 sync s3://bucket-name/data/ data/\
		 --profile $(PROFILE)
	





#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make Dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) labs/data/make_dataset.py


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
