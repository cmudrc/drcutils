"""Shared plotting theme helpers for Matplotlib, Seaborn, pandas, and Plotly."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from importlib import import_module as _import_module
from importlib.resources import files as _resource_files
from typing import Any, Literal

import matplotlib as _mpl
import matplotlib.colors as _mpc
from cycler import cycler as _cycler

from drcutils.brand import BLACK, BRAND_COLORS, get_matplotlib_font_fallbacks
from drcutils.brand.colormaps import (
    drc_cool,
    drc_cool_r,
    drc_dark_diverging,
    drc_dark_diverging_r,
    drc_diverging,
    drc_diverging_r,
    drc_palette,
    drc_palette_r,
    drc_warm,
    drc_warm_r,
)

PlotContext = Literal["paper", "notebook", "talk"]

_PLOT_STYLE_PATH = _resource_files("drcutils") / "data" / "drc.mplstyle"
_PALETTE_KEYS = ["dark_teal", "blue", "orange", "red", "teal", "black"]
_PLOT_PALETTE = [BRAND_COLORS[key] for key in _PALETTE_KEYS]
_STATIC_RC_PARAMS: dict[str, Any] = {
    "axes.axisbelow": True,
    "axes.edgecolor": "#B9C9C7",
    "axes.facecolor": "#FFFFFF",
    "axes.grid": True,
    "axes.grid.axis": "y",
    "axes.grid.which": "major",
    "axes.labelcolor": BLACK,
    "axes.linewidth": 0.8,
    "axes.prop_cycle": _cycler(color=_PLOT_PALETTE),
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.titlecolor": BLACK,
    "errorbar.capsize": 3.0,
    "figure.facecolor": "#FFFFFF",
    "grid.alpha": 1.0,
    "grid.color": "#D9E2E1",
    "grid.linestyle": "-",
    "grid.linewidth": 0.8,
    "image.cmap": drc_diverging.name,
    "legend.facecolor": "#FFFFFF",
    "legend.frameon": False,
    "lines.linewidth": 2.0,
    "lines.markersize": 5.0,
    "patch.edgecolor": "#FFFFFF",
    "savefig.bbox": "tight",
    "savefig.edgecolor": "#FFFFFF",
    "savefig.facecolor": "#FFFFFF",
    "savefig.pad_inches": 0.05,
    "text.color": BLACK,
    "xtick.color": BLACK,
    "xtick.direction": "out",
    "ytick.color": BLACK,
    "ytick.direction": "out",
}
_PLOT_CONTEXTS: dict[PlotContext, dict[str, Any]] = {
    "paper": {
        "font.size": 9.0,
        "axes.titlesize": 10.0,
        "figure.titlesize": 10.0,
        "axes.labelsize": 9.0,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
        "legend.fontsize": 8.0,
        "legend.title_fontsize": 8.0,
        "savefig.dpi": 300,
    },
    "notebook": {
        "font.size": 11.0,
        "axes.titlesize": 12.0,
        "figure.titlesize": 12.0,
        "axes.labelsize": 11.0,
        "xtick.labelsize": 10.0,
        "ytick.labelsize": 10.0,
        "legend.fontsize": 10.0,
        "legend.title_fontsize": 10.0,
        "savefig.dpi": 150,
    },
    "talk": {
        "font.size": 14.0,
        "axes.titlesize": 16.0,
        "figure.titlesize": 16.0,
        "axes.labelsize": 14.0,
        "xtick.labelsize": 12.0,
        "ytick.labelsize": 12.0,
        "legend.fontsize": 12.0,
        "legend.title_fontsize": 12.0,
        "savefig.dpi": 200,
    },
}
_SEABORN_ERROR = (
    "Seaborn is optional for plotting themes. Install with "
    "`pip install drcutils[seaborn]` or `pip install drcutils[visualization]`."
)
_PLOTLY_SEQUENTIAL = drc_cool
_PLOTLY_SEQUENTIAL_MINUS = drc_warm
_PLOTLY_DIVERGING = drc_diverging
_REGISTERED_COLORMAPS = (
    drc_palette,
    drc_palette_r,
    drc_diverging,
    drc_diverging_r,
    drc_dark_diverging,
    drc_dark_diverging_r,
    drc_cool,
    drc_cool_r,
    drc_warm,
    drc_warm_r,
)


def _validate_context(context: str) -> PlotContext:
    if context not in _PLOT_CONTEXTS:
        valid = ", ".join(sorted(_PLOT_CONTEXTS))
        raise ValueError(f"Unknown plotting context '{context}'. Valid contexts: {valid}")
    return context


def _get_font_rcparams() -> dict[str, Any]:
    secondary = get_matplotlib_font_fallbacks()["secondary"]
    return {
        "font.family": ["serif"],
        "font.serif": secondary,
    }


def _get_theme_rcparams(context: PlotContext) -> dict[str, Any]:
    return {
        **_STATIC_RC_PARAMS,
        **get_plot_rcparams(context),
        **_get_font_rcparams(),
    }


def _register_colormaps() -> None:
    for cmap in _REGISTERED_COLORMAPS:
        if cmap.name not in _mpl.colormaps:
            _mpl.colormaps.register(cmap)


def _build_plotly_font_family() -> str:
    fonts = get_matplotlib_font_fallbacks()["secondary"]
    return ", ".join(f'"{font}"' if " " in font else font for font in fonts)


def _sample_colormap_for_plotly(cmap: Any, n: int = 11) -> list[list[Any]]:
    if n < 2:
        raise ValueError("Plotly colorscales require at least two samples.")
    return [[idx / (n - 1), _mpc.to_hex(cmap(idx / (n - 1)))] for idx in range(n)]


def _get_seaborn() -> Any:
    try:
        return _import_module("seaborn")
    except ImportError as exc:
        raise ImportError(_SEABORN_ERROR) from exc


def get_plot_style_path() -> str:
    """Return the packaged Matplotlib style path for the DRC plotting theme."""
    _register_colormaps()
    return str(_PLOT_STYLE_PATH)


def get_plot_palette() -> list[str]:
    """Return the canonical categorical plotting palette."""
    return list(_PLOT_PALETTE)


def get_plot_rcparams(context: PlotContext = "paper") -> dict[str, Any]:
    """Return context-specific rcParams for the DRC plotting theme."""
    context = _validate_context(context)
    return dict(_PLOT_CONTEXTS[context])


def use_plot_style(context: PlotContext = "paper", seaborn: bool = False) -> None:
    """Apply the DRC plotting theme to the current Matplotlib session."""
    context = _validate_context(context)
    _register_colormaps()
    _mpl.style.use(get_plot_style_path())
    _mpl.rcParams.update(_get_theme_rcparams(context))

    if seaborn:
        sns = _get_seaborn()
        sns.set_theme(
            style="whitegrid",
            context=context,
            palette=get_plot_palette(),
            rc=_get_theme_rcparams(context),
        )


@contextmanager
def plot_style_context(
    context: PlotContext = "paper",
    seaborn: bool = False,
) -> Iterator[None]:
    """Temporarily apply the DRC plotting theme within a context manager."""
    with _mpl.rc_context():
        use_plot_style(context=context, seaborn=seaborn)
        yield


def get_plotly_template() -> dict[str, Any]:
    """Return a Plotly template dictionary aligned with the DRC plotting theme."""
    font_family = _build_plotly_font_family()
    grid_color = "#D9E2E1"
    return {
        "layout": {
            "colorway": get_plot_palette(),
            "font": {
                "family": font_family,
                "color": BLACK,
            },
            "paper_bgcolor": "#FFFFFF",
            "plot_bgcolor": "#FFFFFF",
            "xaxis": {
                "gridcolor": grid_color,
                "linecolor": "#B9C9C7",
                "zerolinecolor": grid_color,
                "automargin": True,
                "title": {"standoff": 12},
            },
            "yaxis": {
                "gridcolor": grid_color,
                "linecolor": "#B9C9C7",
                "zerolinecolor": grid_color,
                "automargin": True,
                "title": {"standoff": 12},
            },
            "colorscale": {
                "sequential": _sample_colormap_for_plotly(_PLOTLY_SEQUENTIAL),
                "sequentialminus": _sample_colormap_for_plotly(_PLOTLY_SEQUENTIAL_MINUS),
                "diverging": _sample_colormap_for_plotly(_PLOTLY_DIVERGING),
            },
        }
    }


__all__ = [
    "get_plot_palette",
    "get_plot_rcparams",
    "get_plot_style_path",
    "get_plotly_template",
    "plot_style_context",
    "use_plot_style",
]
