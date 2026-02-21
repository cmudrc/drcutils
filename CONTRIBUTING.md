# Contributing to drcutils

Thanks for helping improve drcutils.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Local Quality Checks

```bash
make fmt
make lint
make type
make test
make docs-build
```

Optional:

```bash
pre-commit install
pre-commit run --all-files
```

## Pull Request Guidelines

- Keep PRs focused and small.
- Add or update tests for behavior changes.
- Update docs when public behavior changes.
- Include a short validation summary (commands run and results).

## Code Style

- Python 3.12+
- Ruff for linting and formatting.
- Mypy for type checking.
- Pytest for tests.
