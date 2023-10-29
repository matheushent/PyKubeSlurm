SHELL:=/bin/bash
PACKAGE_NAME:=pykubeslurm
ROOT_DIR:=$(shell dirname $(shell pwd))

.PHONY: install
install:
	poetry install

.PHONY: mypy
mypy: install
	poetry run mypy ${PACKAGE_NAME} --pretty

.PHONY: lint
lint: install
	poetry run ruff check ${PACKAGE_NAME}

.PHONY: qa
qa: mypy lint test
	echo "All quality checks pass!"


.PHONY: test
test:
	poetry run pytest

.PHONY: format
format: install
	poetry run isort ${PACKAGE_NAME} tests
	poetry run black ${PACKAGE_NAME} tests

.PHONY: local
local: install
	poetry run python pykubeslurm/main.py

.PHONY: docs
docs: install
	poetry run mkdocs build --config-file=docs/mkdocs.yaml

.PHONY: docs-serve
docs-serve: install
	poetry run mkdocs serve --config-file=docs/mkdocs.yaml -a 0.0.0.0:8000 -w docs

.PHONY: charm
charm: install
	charmcraft pack -p ./charm

.PHONY: clean
clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete
	@rm -r .mypy_cache
	@rm -r .pytest_cache

.PHONY: clean-eggs
clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

.PHONY: clean-build
clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info