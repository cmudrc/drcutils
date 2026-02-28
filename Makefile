PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
PIP ?= $(PYTHON) -m pip
PYTEST ?= $(PYTHON) -m pytest
RUFF ?= $(PYTHON) -m ruff
MYPY ?= $(PYTHON) -m mypy
SPHINX ?= $(PYTHON) -m sphinx

.PHONY: install install-dev lint lint-fix fmt fmt-check docstrings-check type test qa coverage examples-static examples-metrics ci docs-build docs-linkcheck docs clean

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

docstrings-check:
	$(RUFF) check src/drcutils --select D

type:
	PYTHONPATH=src $(MYPY) src/drcutils

test:
	PYTHONPATH=src $(PYTEST)

coverage:
	mkdir -p artifacts/coverage
	PYTHONPATH=src $(PYTEST) --cov=src/drcutils --cov-report=term --cov-report=json:artifacts/coverage/coverage.json
	$(PYTHON) scripts/check_coverage_thresholds.py --coverage-json artifacts/coverage/coverage.json
	$(PYTHON) scripts/generate_coverage_badge.py

examples-static:
	PYTHONPATH=src $(PYTHON) scripts/check_example_static_suite.py

examples-metrics:
	PYTHONPATH=src $(PYTHON) scripts/generate_examples_metrics.py
	$(PYTHON) scripts/check_examples_thresholds.py --metrics-json artifacts/examples/examples_metrics.json
	$(PYTHON) scripts/generate_examples_badges.py

qa: lint fmt-check docstrings-check type test

ci: qa coverage examples-static examples-metrics

docs-build:
	PYTHONPATH=src $(SPHINX) -b html docs docs/_build/html -n -W --keep-going -E

docs-linkcheck:
	PYTHONPATH=src $(SPHINX) -b linkcheck docs docs/_build/linkcheck -W --keep-going -E

docs: docs-build

clean:
	rm -rf docs/_build .pytest_cache .mypy_cache .ruff_cache artifacts
