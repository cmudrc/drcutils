PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
PIP ?= $(PYTHON) -m pip
PYTEST ?= $(PYTHON) -m pytest
RUFF ?= $(PYTHON) -m ruff
MYPY ?= $(PYTHON) -m mypy
SPHINX ?= $(PYTHON) -m sphinx
MPLBACKEND ?= Agg

export MPLBACKEND

.PHONY: check-python install dev install-dev lint lint-fix fmt fmt-check docstrings-check type test qa coverage examples-static examples-metrics ci docs-build docs-linkcheck docs clean

check-python:
	@$(PYTHON) -c "import pathlib, sys; print(f'Using Python {sys.version.split()[0]} at {pathlib.Path(sys.executable)}'); raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" || (echo "Python >= 3.12 is required by pyproject.toml"; exit 1)

install:
	$(PIP) install --upgrade pip
	$(PIP) install -e "."

dev:
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

install-dev: dev

lint: check-python
	$(RUFF) check .

lint-fix: check-python
	$(RUFF) check . --fix

fmt: check-python
	$(RUFF) format .

fmt-check: check-python
	$(RUFF) format --check .

docstrings-check: check-python
	$(RUFF) check src/drcutils --select D

type: check-python
	PYTHONPATH=src $(MYPY) src/drcutils

test: check-python
	PYTHONPATH=src $(PYTEST) -q

coverage: check-python
	mkdir -p artifacts/coverage
	PYTHONPATH=src $(PYTEST) -q --cov=src/drcutils --cov-report=term --cov-report=json:artifacts/coverage/coverage.json
	$(PYTHON) scripts/check_coverage_thresholds.py --coverage-json artifacts/coverage/coverage.json
	$(PYTHON) scripts/generate_coverage_badge.py

examples-static: check-python
	PYTHONPATH=src $(PYTHON) scripts/check_example_static_suite.py

examples-metrics: check-python
	PYTHONPATH=src $(PYTHON) scripts/generate_examples_metrics.py
	$(PYTHON) scripts/check_examples_thresholds.py --metrics-json artifacts/examples/examples_metrics.json
	$(PYTHON) scripts/generate_examples_badges.py

qa: lint fmt-check docstrings-check type test docs-build

ci: qa coverage examples-static examples-metrics

docs-build: check-python
	PYTHONPATH=src $(SPHINX) -b html docs docs/_build/html -n -W --keep-going -E

docs-linkcheck: check-python
	PYTHONPATH=src $(SPHINX) -b linkcheck docs docs/_build/linkcheck -W --keep-going -E

docs: docs-build

clean:
	rm -rf docs/_build .pytest_cache .mypy_cache .ruff_cache artifacts
