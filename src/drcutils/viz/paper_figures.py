"""Utilities for exporting paper-ready Matplotlib figures."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any

import matplotlib as _mpl
from matplotlib.figure import Figure

_PRESETS: dict[str, dict[str, float]] = {
    "one_col": {"width": 3.4, "height": 2.2, "font_scale": 1.0},
    "two_col": {"width": 7.0, "height": 3.6, "font_scale": 1.05},
    "slide_16x9": {"width": 10.0, "height": 5.625, "font_scale": 1.25},
}


def get_figure_preset(target: str) -> dict[str, float]:
    """Return figure preset settings for a named target.

    Args:
        target: One of ``one_col``, ``two_col``, or ``slide_16x9``.

    Returns:
        A dictionary with width, height, and font scale.

    Raises:
        ValueError: If target is unknown.
    """
    if target not in _PRESETS:
        valid = ", ".join(sorted(_PRESETS))
        raise ValueError(f"Unknown target '{target}'. Valid targets: {valid}")
    return dict(_PRESETS[target])


@contextmanager
def _style_context(
    embed_fonts: bool,
    font_family: str | None,
    base_fontsize: float | None,
) -> Any:
    """Apply temporary rcParams for export-time typography behavior."""
    updates: dict[str, Any] = {}
    if embed_fonts:
        updates["pdf.fonttype"] = 42
        updates["ps.fonttype"] = 42
        updates["svg.fonttype"] = "none"
    if font_family:
        updates["font.family"] = font_family
    if base_fontsize is not None:
        updates["font.size"] = base_fontsize
    with _mpl.rc_context(updates):
        yield


def _audit_figure(fig: Figure, min_fontsize: float = 6.0) -> list[str]:
    """Collect non-fatal quality warnings for the figure."""
    warnings: list[str] = []

    text_sizes = [
        text.get_fontsize() for text in fig.findobj(match=lambda o: hasattr(o, "get_fontsize"))
    ]
    if text_sizes and min(text_sizes) < min_fontsize:
        warnings.append(
            f"Minimum font size ({min(text_sizes):.2f}) is below recommended {min_fontsize}."
        )

    for idx, ax in enumerate(fig.axes):
        has_data = bool(ax.has_data())
        if has_data and not ax.get_xlabel():
            warnings.append(f"Axis {idx} is missing an x-label.")
        if has_data and not ax.get_ylabel():
            warnings.append(f"Axis {idx} is missing a y-label.")

    try:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        for idx, ax in enumerate(fig.axes):
            legend = ax.get_legend()
            if legend is None:
                continue
            leg_box = legend.get_window_extent(renderer=renderer)
            ax_box = ax.get_window_extent(renderer=renderer)
            if leg_box.overlaps(ax_box):
                warnings.append(f"Axis {idx} legend may overlap plot area.")
    except Exception:
        warnings.append("Figure audit skipped legend-overlap check due to renderer limitations.")

    return warnings


def export_figure(
    fig: Figure,
    outpath_stem: str | Path,
    *,
    targets: list[str] | None = None,
    formats: list[str] | None = None,
    dpi: int = 300,
    transparent: bool = False,
    tight: bool = True,
    font_family: str | None = None,
    base_fontsize: float | None = None,
    embed_fonts: bool = True,
    metadata: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Export a Matplotlib figure for publication presets.

    Args:
        fig: Matplotlib figure object to export.
        outpath_stem: Base output path stem.
        targets: Preset targets to render.
        formats: Output formats such as ``pdf``, ``png``, or ``svg``.
        dpi: Raster resolution for bitmap outputs.
        transparent: Whether to export with transparent background.
        tight: Whether to save with tight bounding boxes.
        font_family: Optional font family override.
        base_fontsize: Optional base font size override.
        embed_fonts: Whether to configure embedded/export-friendly fonts.
        metadata: Optional metadata mapping passed to savefig.

    Returns:
        A dictionary containing generated file paths, resolved settings, and warnings.
    """
    targets = ["one_col"] if targets is None else targets
    formats = ["pdf", "png"] if formats is None else formats

    stem = Path(outpath_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)

    output_files: list[Path] = []
    resolved_settings: dict[str, dict[str, Any]] = {}
    warnings = _audit_figure(fig)

    for target in targets:
        preset = get_figure_preset(target)
        width = preset["width"]
        height = preset["height"]
        font_scale = preset["font_scale"]
        resolved_fontsize = (
            base_fontsize if base_fontsize is not None else _mpl.rcParams["font.size"]
        ) * font_scale

        with _style_context(
            embed_fonts=embed_fonts, font_family=font_family, base_fontsize=resolved_fontsize
        ):
            fig.set_size_inches(width, height)
            resolved_settings[target] = {
                "size_inches": [width, height],
                "font_scale": font_scale,
                "fontsize": resolved_fontsize,
                "transparent": transparent,
                "tight": tight,
            }
            for fmt in formats:
                ext = fmt.lower()
                out_path = stem.parent / f"{stem.name}__{target}.{ext}"
                save_kwargs: dict[str, Any] = {
                    "format": ext,
                    "transparent": transparent,
                    "metadata": metadata,
                }
                if ext in {"png", "jpg", "jpeg", "tif", "tiff"}:
                    save_kwargs["dpi"] = dpi
                if tight:
                    save_kwargs["bbox_inches"] = "tight"
                fig.savefig(out_path, **save_kwargs)
                output_files.append(out_path)

    return {
        "files": output_files,
        "settings": resolved_settings,
        "warnings": warnings,
    }
