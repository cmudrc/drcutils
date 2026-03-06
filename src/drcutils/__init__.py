"""Public package exports for drcutils."""

from . import brand, data, doe, runtime, viz
from .brand import COLORS, flag, watermark
from .data import convert
from .doe import analyze_doe_response, compute_main_effects, fit_screening_model, generate_doe
from .runtime import is_google_colab, is_notebook
from .viz import export_figure, get_figure_preset, visualize_network, visualize_stl

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "COLORS",
    "analyze_doe_response",
    "brand",
    "compute_main_effects",
    "convert",
    "data",
    "doe",
    "export_figure",
    "flag",
    "fit_screening_model",
    "generate_doe",
    "get_figure_preset",
    "is_google_colab",
    "is_notebook",
    "runtime",
    "viz",
    "visualize_network",
    "visualize_stl",
    "watermark",
]
