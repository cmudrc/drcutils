from . import brand, cad, colormaps, env, magic, ml
from .brand import COLORS, flag, watermark
from .cad import visualize_stl
from .env import is_google_colab, is_notebook
from .magic import convert
from .ml import visualize_network

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "COLORS",
    "brand",
    "cad",
    "colormaps",
    "convert",
    "env",
    "flag",
    "is_google_colab",
    "is_notebook",
    "magic",
    "ml",
    "visualize_network",
    "visualize_stl",
    "watermark",
]
