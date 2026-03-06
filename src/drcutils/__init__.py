"""Public package exports for drcutils."""

from . import brand, data, doe, runtime, sequence, stats, viz
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
from .sequence import (
    DecodeResult,
    DiscreteHMMResult,
    GaussianHMMResult,
    MarkovChainResult,
    decode_hmm,
    embed_text,
    fit_discrete_hmm,
    fit_gaussian_hmm,
    fit_markov_chain,
    fit_text_gaussian_hmm,
    plot_state_graph,
    plot_transition_matrix,
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
    "DecodeResult",
    "DiscreteHMMResult",
    "GaussianHMMResult",
    "MarkovChainResult",
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
    "fit_discrete_hmm",
    "fit_gaussian_hmm",
    "fit_markov_chain",
    "export_figure",
    "flag",
    "fit_screening_model",
    "fit_text_gaussian_hmm",
    "generate_doe",
    "generate_codebook",
    "get_figure_preset",
    "decode_hmm",
    "embed_text",
    "is_google_colab",
    "is_notebook",
    "minimum_detectable_effect",
    "permutation_test",
    "plot_state_graph",
    "plot_transition_matrix",
    "power_curve",
    "profile_dataframe",
    "rank_tests_one_stop",
    "runtime",
    "sequence",
    "stats",
    "validate_dataframe",
    "viz",
    "visualize_network",
    "visualize_stl",
    "watermark",
    "write_run_manifest",
]
