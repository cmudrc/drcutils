"""Preferred visualization namespace for plotting and figure helpers."""

from .cad import visualize_stl
from .ml import visualize_network
from .paper_figures import export_figure, get_figure_preset
from .plotting import (
    get_plot_palette,
    get_plot_rcparams,
    get_plot_style_path,
    get_plotly_template,
    plot_style_context,
    use_plot_style,
)

__all__ = [
    "export_figure",
    "get_figure_preset",
    "get_plot_palette",
    "get_plot_rcparams",
    "get_plot_style_path",
    "get_plotly_template",
    "plot_style_context",
    "use_plot_style",
    "visualize_network",
    "visualize_stl",
]
