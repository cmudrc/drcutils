"""Public package exports for drcutils."""

from . import brand, cad, colormaps, dataset, env, magic, ml, power, repro
from .brand import COLORS, flag, watermark
from .cad import visualize_stl
from .dataset import generate_codebook, profile_dataframe, validate_dataframe
from .doe import analyze_doe_response, compute_main_effects, fit_screening_model, generate_doe
from .env import is_google_colab, is_notebook
from .magic import convert
from .ml import visualize_network
from .power import estimate_sample_size, minimum_detectable_effect, power_curve
from .repro import attach_provenance, capture_run_context, write_run_manifest
from .stats import bootstrap_ci, permutation_test, rank_tests_one_stop
from .viz import export_figure, get_figure_preset

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "COLORS",
    "analyze_doe_response",
    "attach_provenance",
    "bootstrap_ci",
    "brand",
    "cad",
    "capture_run_context",
    "colormaps",
    "compute_main_effects",
    "convert",
    "dataset",
    "env",
    "estimate_sample_size",
    "export_figure",
    "flag",
    "fit_screening_model",
    "generate_doe",
    "generate_codebook",
    "get_figure_preset",
    "is_google_colab",
    "is_notebook",
    "magic",
    "minimum_detectable_effect",
    "ml",
    "power",
    "power_curve",
    "permutation_test",
    "profile_dataframe",
    "rank_tests_one_stop",
    "repro",
    "validate_dataframe",
    "visualize_network",
    "visualize_stl",
    "watermark",
    "write_run_manifest",
]
