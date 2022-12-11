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

## Stack Listing
- `brand_stack`, for working with our brand elements
  - imports `numpy-stl`, `matplotlib.colors`, `svpathtools` and `Pillow`
  - contains list `COLORS`, which contains the brand colors as hex codes. 
  - contains object `logo_only`, which has attributes:
    - `SVG_PATH`, path to the logo_only .svg file.
    - `SVG_PATH`, path to the logo_only .png file.
    - `STL_PATH`, path to the logo_only .stl file
    - `SVG_OBJECT`, object containing data on the svg-style curves that make up the logo (from the `svgpathtools` library)
    - `IMAGE_OBJECT`, object containing a raster-style image of the logo (`PIL.Image` from the `Pillow` library)
    - `MESH_OBJECT`, object containing an stl-style mesh of the logo (`Mesh` object type from `numpy-stl` library)
    
- `data_stack`, for working with data
  - imports `numpy` and `pandas`
- `hack_stack`, for working on just about anything
  - imports `numpy`, `pandas`, `datasets`, `keras`, `matplotlib.pyplot`, `sklearn`, and `gradio`
- `hf_stack`, for working with Huggingface
  - imports `huggingface_hub`, `datasets`, and `gradio`
- `plotting_stack`
  - imports `matplotlib.colors` and `matplotlib.pyplot`
  - Contains two colormaps that align with our lab brand (`hamster_colormap` and `diverging_hamster_colormap`)
- `stats_stack`
  - imports `pandas`, `scipy.stats`, and `statsmodels`
