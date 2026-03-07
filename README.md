# drcutils
[![CI](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml/badge.svg)](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml)
[![Coverage](https://raw.githubusercontent.com/cmudrc/drcutils/main/.github/badges/coverage.svg)](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml)
[![Examples Passing](https://raw.githubusercontent.com/cmudrc/drcutils/main/.github/badges/examples-passing.svg)](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml)
[![Public API In Examples](https://raw.githubusercontent.com/cmudrc/drcutils/main/.github/badges/examples-api-coverage.svg)](https://github.com/cmudrc/drcutils/actions/workflows/ci.yml)
[![Docs](https://github.com/cmudrc/drcutils/actions/workflows/docs-pages.yml/badge.svg)](https://github.com/cmudrc/drcutils/actions/workflows/docs-pages.yml)

`drcutils` is a shared utility package for Design Research Collective lab members.

It is intended primarily for internal lab workflows where consistent branding,
figure export, and lightweight runtime/data helpers are needed across projects.

## Overview

This package currently focuses on:

- DRC brand assets, palettes, and watermarking helpers
- publication-ready figure export presets
- CAD and model-visualization wrappers
- file conversion and runtime environment detection utilities

## Quickstart

Requires Python 3.12+.
Reproducible release installs are pinned to Python `3.12.12` (`.python-version`).

```bash
python -m venv .venv
source .venv/bin/activate
make dev
make test
```

## Quick Usage

```python
import matplotlib.pyplot as plt

from drcutils.data import convert
from drcutils.runtime import is_notebook
from drcutils.viz import export_figure

convert("inputs/data.csv", "artifacts/data.json")

fig, ax = plt.subplots()
ax.plot([0, 1, 2], [0, 1, 4])

result = export_figure(
    fig,
    "artifacts/figures/main_result",
    targets=["one_col", "slide_16x9"],
    formats=["pdf", "png"],
)

print(is_notebook())
print(result["files"])
```

## Examples

- Basic functionality:
  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/basic_functionality.ipynb)
- Advanced example:
  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/logo_adventures.ipynb)

## Docs

See the [published documentation](https://cmudrc.github.io/drcutils/) for usage guides and API reference.

Build docs locally with:

```bash
make docs-build
```

## Contributing

Contribution workflow and quality gates are documented in
[CONTRIBUTING.md](https://github.com/cmudrc/drcutils/blob/main/CONTRIBUTING.md).
