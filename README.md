# `drcutils`
Python package with useful utilities for the lab

## Installation
To install this package, run:
```bash
pip install git+https://github.com/cmudrc/drcutils.git
```

## Usage
The package is organized according to several software stacks, each of which contains utilities for a given type of task. In most cases, you'll want to import everything in the stack by running
```python
from drcutils.STACK_NAME import *
```
This will load additional (and useful!) libraries, objects, functions, and constants. Replace `STACK_NAME` with the name of a stack of your choice. 

## Available Stacks

### `hack_stack`, for working on just about anything 

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/hack_stack.ipynb) 
- imports `numpy`, `pandas`, `datasets`, `keras`, `matplotlib.pyplot`, `sklearn`, and `gradio`
- `visualize_network`, a function for visualizing neural network architectures.
<img width="1016" alt="Screenshot 2022-12-17 at 1 58 25 PM" src="https://user-images.githubusercontent.com/6705753/208257417-7c6d470e-714f-455c-9ed0-22912934e710.png">

### `hf_stack`, for making data, models, and demos with Huggingface 

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/hf_stack.ipynb) 
- imports `huggingface_hub`, `datasets`, and `gradio`, `numpy`, `PIL`, `pandas`, `plotly.express`, `plotly.graph_objects`

### `plotting_stack`, for making beautiful figures 

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/plotting_stack.ipynb) 
- imports `matplotlib.colors`, `matplotlib.pyplot`, `numpy-stl`, `svpathtools` and `Pillow`
- Contains two colormaps that align with our lab brand (`hamster_colormap` and `diverging_hamster_colormap`)
- contains `COLORS`, a list which contains the brand colors as hex codes. 
- contains object `logo_only`, which has attributes:
  - `SVG_PATH`, path to the logo-only .svg file.
  - `PNG_PATH`, path to the logo-only .png file.
  - `STL_PATH`, path to the logo-only .stl file
  - `SVG_OBJECT`, object containing data on the svg-style curves that make up the logo (from the `svgpathtools` library)
  - `IMAGE_OBJECT`, object containing a raster-style image of the logo (`PIL.Image` from the `Pillow` library)
  - `MESH_OBJECT`, object containing an stl-style mesh of the logo (`Mesh` object type from `numpy-stl` library)
- contains object `horizontal_logo`, which has attributes:
  - `PNG_PATH`, path to the horizontal layout of the logo as a .png file.
  - `IMAGE_OBJECT`, object containing a raster-style image of the horizontal layout of the logo (`PIL.Image` from the `Pillow` library)
- contains object `stacked_logo`, which has attributes:
  - `PNG_PATH`, path to the stacked layout of the logo as a .png file.
  - `IMAGE_OBJECT`, object containing a raster-style image of the stacked layout of the logo (`PIL.Image` from the `Pillow` library)    

### `stats_stack`, for doing rigorous statistics 

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmudrc/drcutils/blob/main/examples/stats_stack.ipynb) 
- imports `pandas`, `scipy.stats`, and `statsmodels`
