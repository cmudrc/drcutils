# drcutils

Utility functions for design research workflows, including branding assets,
file conversion helpers, colormaps, CAD visualization, and neural-network
visualization wrappers.

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
from drcutils.brand import flag
from drcutils.magic import convert

# Generate a brand flag image.
image = flag()
image.save("flag.png")

# Convert tabular files.
convert("data.csv", "data.json")
```

```python
from drcutils.cad import visualize_stl

fig = visualize_stl("model.stl", color="#58B7BB")
fig.show()
```

```python
from drcutils.ml import visualize_network

visualize_network("model.onnx")
```

## Examples

- Basic functionality:
  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/basic_functionality.ipynb)
- Advanced example:
  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/logo_adventures.ipynb)

## Development Commands

```bash
make install-dev
make qa
make docs-build
```

## Notes

The package currently ships brand image assets directly in `drcutils/data/`.
If package size becomes an issue, a follow-up can move large patterned images
to compressed/optional artifacts.
