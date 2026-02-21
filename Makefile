PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
PIP ?= $(PYTHON) -m pip
PYTEST ?= $(PYTHON) -m pytest
RUFF ?= $(PYTHON) -m ruff
MYPY ?= $(PYTHON) -m mypy
SPHINX ?= $(PYTHON) -m sphinx

.PHONY: install install-dev lint lint-fix fmt fmt-check type test qa docs-build docs-linkcheck docs clean

install:
	$(PIP) install --upgrade pip
	$(PIP) install -e "."

install-dev:
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

lint:
	$(RUFF) check .

lint-fix:
	$(RUFF) check . --fix

fmt:
	$(RUFF) format .

fmt-check:
	$(RUFF) format --check .

type:
	$(MYPY) drcutils

test:
	$(PYTEST)

qa: lint fmt-check type test

docs-build:
	$(SPHINX) -b html docs docs/_build/html -n -W --keep-going -E

docs-linkcheck:
	$(SPHINX) -b linkcheck docs docs/_build/linkcheck -W --keep-going -E

docs: docs-build

clean:
	rm -rf docs/_build .pytest_cache .mypy_cache .ruff_cache
