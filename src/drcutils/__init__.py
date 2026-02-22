"""Public package exports for drcutils."""

from . import brand, cad, colormaps, env, magic, ml
from .brand import COLORS, flag, watermark
from .cad import visualize_stl
from .doe import generate_doe
from .env import is_google_colab, is_notebook
from .magic import convert
from .ml import visualize_network
from .stats import bootstrap_ci, permutation_test, rank_tests_one_stop
from .viz import export_figure, get_figure_preset

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "COLORS",
    "bootstrap_ci",
    "brand",
    "cad",
    "colormaps",
    "convert",
    "env",
    "export_figure",
    "flag",
    "generate_doe",
    "get_figure_preset",
    "is_google_colab",
    "is_notebook",
    "magic",
    "ml",
    "permutation_test",
    "rank_tests_one_stop",
    "visualize_network",
    "visualize_stl",
    "watermark",
]
