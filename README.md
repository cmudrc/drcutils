# drcutils
[![CI](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml/badge.svg)](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml)
[![Coverage](.github/badges/coverage.svg)](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml)
[![Examples Passing](.github/badges/examples-passing.svg)](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml)
[![Public API In Examples](.github/badges/examples-api-coverage.svg)](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml)
[![Unit Tests](https://github.com/cmudrc/drcutils/actions/workflows/tests.yml/badge.svg)](https://github.com/cmudrc/drcutils/actions/workflows/tests.yml)
[![Docs](https://github.com/cmudrc/drcutils/actions/workflows/docs.yml/badge.svg)](https://github.com/cmudrc/drcutils/actions/workflows/docs.yml)

Utility functions for design research workflows, including branding assets,
file conversion helpers, colormaps, CAD visualization, neural-network
visualization wrappers, and new research-oriented DOE/stats/viz helpers.

## Installation

```bash
pip install drcutils
```

For contributor tooling:

```bash
pip install -e ".[dev]"
```

## Quick Usage

```python
from drcutils.viz import export_figure
from drcutils.doe import generate_doe
from drcutils.stats import bootstrap_ci

# Export publication-ready figures.
result = export_figure(fig, "artifacts/figures/plot", targets=["one_col", "slide_16x9"])

# Generate a DOE table.
doe = generate_doe(kind="lhs", factors={"x": (0.0, 1.0), "y": (10.0, 20.0)}, n_samples=12)

# Compute bootstrap interval.
ci = bootstrap_ci([1, 2, 3, 4, 5], stat="mean", seed=0)
```

## Research Lab Additions

```python
from drcutils import (
    analyze_doe_response,
    capture_run_context,
    estimate_sample_size,
    validate_dataframe,
)

context = capture_run_context(seed=7, input_paths=["data/study.csv"])
validation = validate_dataframe(df, {"participant_id": {"unique": True, "nullable": False}})
power = estimate_sample_size(0.5, test="two_sample_t")
analysis = analyze_doe_response(doe_df, response="yield")
```

Power analysis and DOE screening models require the optional stats extras:

```bash
pip install drcutils[stats]
```

## Examples

- Basic functionality:
  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/basic_functionality.ipynb)
- Advanced example:
  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/logo_adventures.ipynb)

## Development Commands

```bash
make install-dev
make ci
make docs-build
```

## Optional Extras

- DOE extras: `pip install drcutils[doe]`
- Stats extras: `pip install drcutils[stats]`
- Plotly extras: `pip install drcutils[plotly]`
