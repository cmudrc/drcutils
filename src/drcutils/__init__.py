"""Public package exports for drcutils."""

from . import brand, data, doe, runtime, stats, viz
from .brand import COLORS, flag, watermark
from .data import convert, generate_codebook, profile_dataframe, validate_dataframe
from .doe import analyze_doe_response, compute_main_effects, fit_screening_model, generate_doe
from .runtime import (
    attach_provenance,
    capture_run_context,
    is_google_colab,
    is_notebook,
    write_run_manifest,
)
from .stats import (
    bootstrap_ci,
    estimate_sample_size,
    minimum_detectable_effect,
    permutation_test,
    power_curve,
    rank_tests_one_stop,
)
from .viz import export_figure, get_figure_preset, visualize_network, visualize_stl

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "COLORS",
    "analyze_doe_response",
    "attach_provenance",
    "bootstrap_ci",
    "brand",
    "capture_run_context",
    "compute_main_effects",
    "convert",
    "data",
    "doe",
    "estimate_sample_size",
    "export_figure",
    "flag",
    "fit_screening_model",
    "generate_doe",
    "generate_codebook",
    "get_figure_preset",
    "is_google_colab",
    "is_notebook",
    "minimum_detectable_effect",
    "permutation_test",
    "power_curve",
    "profile_dataframe",
    "rank_tests_one_stop",
    "runtime",
    "stats",
    "validate_dataframe",
    "viz",
    "visualize_network",
    "visualize_stl",
    "watermark",
    "write_run_manifest",
]
