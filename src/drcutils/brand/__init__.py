"""Brand assets and image utilities for DRC visuals."""

from __future__ import annotations

from collections.abc import Sequence
from importlib import import_module as _import_module
from importlib.resources import files as _resource_files
from os import PathLike
from typing import Literal

import matplotlib.colors as _mpc
import numpy as _np
from PIL import Image as _Image

LogoLayout = Literal["horizontal", "stacked", "symbol"]
PatternVariant = Literal["full", "grey", "white"]
ScribbleWeight = Literal["thin", "thick"]

BLACK = "#000000"
DARK_TEAL = "#1A4C49"
TEAL = "#4D8687"
BLUE = "#57B7BA"
ORANGE = "#EA8534"
RED = "#DF5127"

#: Canonical DRC palette in display order.
COLORS = [BLACK, DARK_TEAL, TEAL, BLUE, ORANGE, RED]

#: Semantic palette map for direct lookup in plotting and style code.
BRAND_COLORS = {
    "black": BLACK,
    "dark_teal": DARK_TEAL,
    "teal": TEAL,
    "blue": BLUE,
    "orange": ORANGE,
    "red": RED,
}

PRIMARY_FONT_FAMILY = "Magdelin"
SECONDARY_FONT_FAMILY = "Zilla Slab"
PRIMARY_FONT_USAGE = "ALL CAPS headers"
SECONDARY_FONT_USAGE = "body text"

_DATA_DIR = _resource_files("drcutils") / "data"
_BRAND_ASSETS_DIR = _DATA_DIR / "brand_assets"
_RESAMPLING = getattr(_Image, "Resampling", _Image)

_LOGO_VARIANTS = {
    "horizontal": {
        "full": "full.png",
        "black": "black.png",
        "dark_teal": "dark_teal.png",
        "red": "red.png",
        "white": "white.png",
    },
    "stacked": {
        "full": "full.png",
        "black": "black.png",
        "dark_teal": "dark_teal.png",
        "red": "red.png",
        "white": "white.png",
    },
    "symbol": {
        "full": "full.png",
        "black": "black.png",
        "dark_teal": "dark_teal.png",
        "blue": "blue.png",
        "teal": "teal.png",
        "orange": "orange.png",
        "red": "red.png",
        "white": "white.png",
    },
}
_ON_BLACK_LOGOS = {
    "horizontal": "horizontal.png",
    "stacked": "stacked.png",
    "symbol": "symbol.png",
}
_PATTERNS = {"full": "full.png", "grey": "grey.png", "white": "white.png"}
_CIRCLE_COLORS = {
    "blue": "blue.png",
    "dark_teal": "dark_teal.png",
    "orange": "orange.png",
    "red": "red.png",
    "teal": "teal.png",
    "white": "white.png",
}

#: Path to an SVG of the symbol logo.
LOGO_ONLY_SVG = str(_DATA_DIR / "logo.svg")
#: Path to a PNG of the full-color symbol logo.
LOGO_ONLY_PNG = str(_BRAND_ASSETS_DIR / "logos" / "symbol" / "full.png")
#: Path to an STL of the symbol logo.
LOGO_ONLY_STL = str(_DATA_DIR / "logo.stl")
#: Path to a PNG of the full-color horizontal logo.
HORIZONTAL_LOGO_PNG = str(_BRAND_ASSETS_DIR / "logos" / "horizontal" / "full.png")
#: Path to a PNG of the full-color stacked logo.
STACKED_LOGO_PNG = str(_BRAND_ASSETS_DIR / "logos" / "stacked" / "full.png")
#: Path to the white pattern PNG.
WHITE_PATTERN_PNG = str(_BRAND_ASSETS_DIR / "patterns" / "white.png")
#: Path to the grey pattern PNG.
GREY_PATTERN_PNG = str(_BRAND_ASSETS_DIR / "patterns" / "grey.png")
#: Path to the full-color pattern PNG.
COLOR_PATTERN_PNG = str(_BRAND_ASSETS_DIR / "patterns" / "full.png")


def _normalize_key(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _normalize_color_key(value: str) -> str:
    normalized = _normalize_key(value)
    if normalized == "gray":
        return "grey"
    return normalized


def get_logo_path(
    layout: str,
    variant: str,
    on_black: bool = False,
    fmt: str = "png",
) -> str:
    """Resolve the canonical path for a packaged logo variant."""
    layout_key = _normalize_key(layout)
    if layout_key not in _LOGO_VARIANTS:
        allowed_layouts = ", ".join(sorted(_LOGO_VARIANTS))
        raise ValueError(f"Unsupported logo layout '{layout}'. Choose from: {allowed_layouts}.")

    if fmt.lower() != "png":
        raise ValueError("Only PNG logo assets are packaged.")

    if on_black:
        return str(_BRAND_ASSETS_DIR / "logos" / "on_black" / _ON_BLACK_LOGOS[layout_key])

    variant_key = _normalize_color_key(variant)
    if variant_key == "auto":
        variant_key = "full"
    allowed_variants = _LOGO_VARIANTS[layout_key]
    if variant_key not in allowed_variants:
        valid = ", ".join(sorted(allowed_variants))
        raise ValueError(
            f"Unsupported variant '{variant}' for layout '{layout_key}'. Choose from: {valid}."
        )
    return str(_BRAND_ASSETS_DIR / "logos" / layout_key / allowed_variants[variant_key])


def get_pattern_path(variant: str) -> str:
    """Resolve the canonical path for packaged pattern imagery."""
    variant_key = _normalize_color_key(variant)
    if variant_key not in _PATTERNS:
        valid = ", ".join(sorted(_PATTERNS))
        raise ValueError(f"Unsupported pattern variant '{variant}'. Choose from: {valid}.")
    return str(_BRAND_ASSETS_DIR / "patterns" / _PATTERNS[variant_key])


def get_gradient_paths() -> list[str]:
    """Return ordered packaged gradient asset paths."""
    return [str(_BRAND_ASSETS_DIR / "gradients" / f"{idx:02d}.png") for idx in range(1, 7)]


def get_circle_graphic_path(color: str) -> str:
    """Resolve the canonical path for a packaged circle graphic."""
    color_key = _normalize_color_key(color)
    if color_key not in _CIRCLE_COLORS:
        valid = ", ".join(sorted(_CIRCLE_COLORS))
        raise ValueError(f"Unsupported circle color '{color}'. Choose from: {valid}.")
    return str(_BRAND_ASSETS_DIR / "circles" / _CIRCLE_COLORS[color_key])


def get_scribble_path(weight: str, color: str) -> str:
    """Resolve the canonical path for a packaged scribble graphic."""
    weight_key = _normalize_key(weight)
    if weight_key not in {"thin", "thick"}:
        raise ValueError("Scribble weight must be 'thin' or 'thick'.")

    color_key = _normalize_color_key(color)
    if color_key not in _CIRCLE_COLORS:
        valid = ", ".join(sorted(_CIRCLE_COLORS))
        raise ValueError(f"Unsupported scribble color '{color}'. Choose from: {valid}.")
    return str(_BRAND_ASSETS_DIR / "scribbles" / weight_key / f"{color_key}.png")


def get_matplotlib_font_fallbacks() -> dict[str, list[str]]:
    """Return recommended Matplotlib font fallback stacks."""
    return {
        "primary": [PRIMARY_FONT_FAMILY, "Arial", "Helvetica", "sans-serif"],
        "secondary": [SECONDARY_FONT_FAMILY, "Georgia", "Times New Roman", "serif"],
    }


def _parse_flag_size(size: Sequence[object] | None) -> tuple[list[int], int]:
    if size is None:
        return [50, 10, 10, 10, 10, 10], 100
    if not isinstance(size, (list, tuple)) or len(size) != 2:
        raise ValueError(
            "size must be a 2-item list/tuple: [color_widths, height] or [height, color_widths]."
        )

    first, second = size
    if isinstance(first, int) and isinstance(second, (list, tuple)):
        height = first
        color_widths = second
    elif isinstance(second, int) and isinstance(first, (list, tuple)):
        color_widths = first
        height = second
    else:
        raise ValueError("size must contain one int and one list/tuple of color widths.")

    if not isinstance(height, int) or height <= 0:
        raise ValueError("height must be a positive integer.")

    parsed_widths: list[int] = []
    for idx, width in enumerate(color_widths):
        if not isinstance(width, int) or width <= 0:
            raise ValueError(f"color width at index {idx} must be a positive integer.")
        parsed_widths.append(width)

    if len(parsed_widths) != len(COLORS):
        raise ValueError(f"Expected {len(COLORS)} color widths; received {len(parsed_widths)}.")

    return parsed_widths, height


def _parse_watermark_box(
    box: Sequence[float | None] | None,
) -> tuple[float, float, float | None, float | None]:
    raw = [0.0, 0.0, 0.10, None] if box is None else list(box)
    if len(raw) != 4:
        raise ValueError("box must be a 4-item sequence: [x, y, width_ratio, height_ratio].")

    x_raw, y_raw, width_raw, height_raw = raw
    if x_raw is None or y_raw is None:
        raise ValueError("box x and y positions must be numeric values in [0, 1].")

    x = float(x_raw)
    y = float(y_raw)
    if not (0.0 <= x <= 1.0) or not (0.0 <= y <= 1.0):
        raise ValueError("box x and y must be in [0, 1].")

    width_ratio: float | None = None
    height_ratio: float | None = None
    if width_raw is not None:
        width_ratio = float(width_raw)
        if not (0.0 < width_ratio <= 1.0):
            raise ValueError("box width_ratio must be in (0, 1].")
    if height_raw is not None:
        height_ratio = float(height_raw)
        if not (0.0 < height_ratio <= 1.0):
            raise ValueError("box height_ratio must be in (0, 1].")

    return x, y, width_ratio, height_ratio


def _resize_logo(
    source_size: tuple[int, int],
    logo_image: _Image.Image,
    width_ratio: float | None,
    height_ratio: float | None,
) -> _Image.Image:
    source_width, source_height = source_size
    logo_width, logo_height = logo_image.size

    if width_ratio is None and height_ratio is None:
        return logo_image.copy()
    if width_ratio is None and height_ratio is not None:
        target_height = max(1, int(round(source_height * height_ratio)))
        target_width = max(1, int(round(logo_width * target_height / logo_height)))
        return logo_image.resize((target_width, target_height), _RESAMPLING.LANCZOS)
    if width_ratio is not None and height_ratio is None:
        target_width = max(1, int(round(source_width * width_ratio)))
        target_height = max(1, int(round(logo_height * target_width / logo_width)))
        return logo_image.resize((target_width, target_height), _RESAMPLING.LANCZOS)

    target_width = max(1, int(round(source_width * float(width_ratio))))
    target_height = max(1, int(round(source_height * float(height_ratio))))
    return logo_image.resize((target_width, target_height), _RESAMPLING.LANCZOS)


def _is_dark_region(
    source_rgba: _Image.Image,
    x_position: int,
    y_position: int,
    width: int,
    height: int,
) -> bool:
    x0 = max(0, x_position)
    y0 = max(0, y_position)
    x1 = min(source_rgba.size[0], x_position + width)
    y1 = min(source_rgba.size[1], y_position + height)
    if x1 <= x0 or y1 <= y0:
        return False

    region = source_rgba.crop((x0, y0, x1, y1)).convert("RGB")
    region_array = _np.asarray(region, dtype=float)
    if region_array.size == 0:
        return False
    luminance = (
        0.2126 * region_array[..., 0]
        + 0.7152 * region_array[..., 1]
        + 0.0722 * region_array[..., 2]
    )
    return float(luminance.mean()) < 110.0


def flag(
    output_filepath: str | bytes | PathLike | None = None,
    size: Sequence[object] | None = None,
):
    """Create a DRC color flag image."""
    color_widths, height = _parse_flag_size(size)
    rgb_colors = [_np.array(_mpc.to_rgb(c)) for c in COLORS]

    color_row: list[_np.ndarray] = []
    for idx, color_width in enumerate(color_widths):
        color_row.extend([rgb_colors[idx]] * color_width)

    pixel_data = _np.uint8(_np.array([color_row] * height) * 255)
    flag_image = _Image.fromarray(pixel_data, mode="RGB")

    if output_filepath is None:
        return flag_image

    flag_image.save(output_filepath)
    return None


def watermark(
    filepath: str | bytes | PathLike,
    output_filepath: str | bytes | PathLike | None = None,
    watermark_filepath: str | bytes | PathLike | None = None,
    box: Sequence[float | None] | None = None,
    *,
    logo_layout: str = "stacked",
    logo_variant: str = "auto",
    on_black: bool | Literal["auto"] = "auto",
) -> None:
    """Watermark an image using packaged DRC assets or a custom watermark file."""
    x, y, width_ratio, height_ratio = _parse_watermark_box(box)
    source_image = _Image.open(filepath)
    source_rgba = source_image.convert("RGBA")

    x_position = int(round(source_rgba.size[0] * x))
    y_position = int(round(source_rgba.size[1] * y))

    if watermark_filepath is not None:
        logo_image = _Image.open(watermark_filepath).convert("RGBA")
    else:
        variant_key = _normalize_color_key(logo_variant)
        if variant_key == "auto":
            variant_key = "full"

        if on_black == "auto":
            probe_logo = _Image.open(get_logo_path(logo_layout, variant_key, on_black=False)).convert(
                "RGBA"
            )
            probe_resized = _resize_logo(source_rgba.size, probe_logo, width_ratio, height_ratio)
            use_on_black = _is_dark_region(
                source_rgba,
                x_position,
                y_position,
                probe_resized.size[0],
                probe_resized.size[1],
            )
        elif isinstance(on_black, bool):
            use_on_black = on_black
        else:
            raise ValueError("on_black must be True, False, or 'auto'.")

        logo_path = get_logo_path(logo_layout, variant_key, on_black=use_on_black)
        logo_image = _Image.open(logo_path).convert("RGBA")

    resized_logo = _resize_logo(source_rgba.size, logo_image, width_ratio, height_ratio)

    overlay = _Image.new("RGBA", source_rgba.size, (0, 0, 0, 0))
    overlay.paste(resized_logo, (x_position, y_position), resized_logo)
    composited = _Image.alpha_composite(source_rgba, overlay)

    if source_image.mode == "RGBA":
        output_image = composited
    else:
        output_image = composited.convert(source_image.mode)

    target_path = filepath if output_filepath is None else output_filepath
    output_image.save(target_path)


def __getattr__(name: str) -> object:
    if name == "colormaps":
        return _import_module(".colormaps", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "BLACK",
    "BLUE",
    "BRAND_COLORS",
    "COLORS",
    "COLOR_PATTERN_PNG",
    "DARK_TEAL",
    "GREY_PATTERN_PNG",
    "HORIZONTAL_LOGO_PNG",
    "LOGO_ONLY_PNG",
    "LOGO_ONLY_STL",
    "LOGO_ONLY_SVG",
    "LogoLayout",
    "ORANGE",
    "PatternVariant",
    "PRIMARY_FONT_FAMILY",
    "PRIMARY_FONT_USAGE",
    "RED",
    "SECONDARY_FONT_FAMILY",
    "SECONDARY_FONT_USAGE",
    "STACKED_LOGO_PNG",
    "ScribbleWeight",
    "TEAL",
    "WHITE_PATTERN_PNG",
    "colormaps",
    "flag",
    "get_circle_graphic_path",
    "get_gradient_paths",
    "get_logo_path",
    "get_matplotlib_font_fallbacks",
    "get_pattern_path",
    "get_scribble_path",
    "watermark",
]
