from __future__ import annotations

from collections.abc import Sequence
from importlib.resources import files as _resource_files
from os import PathLike

import matplotlib.colors as _mpc
import numpy as _np
from PIL import Image as _Image

#: The colors of the DRC brand
COLORS = [
    "#000000",
    "#1A4C49",
    "#4C8687",
    "#58B7BB",
    "#EA8534",
    "#DF5227",
]

_DATA_DIR = _resource_files("drcutils") / "data"

#: Path to an SVG of logo
LOGO_ONLY_SVG = str(_DATA_DIR / "logo.svg")

#: Path to a PNG of logo
LOGO_ONLY_PNG = str(_DATA_DIR / "logo.png")

#: Path to an STL of logo
LOGO_ONLY_STL = str(_DATA_DIR / "logo.stl")

#: Path to a PNG of the horizontal logo
HORIZONTAL_LOGO_PNG = str(_DATA_DIR / "horizontal.png")

#: Path to a PNG of the stacked logo
STACKED_LOGO_PNG = str(_DATA_DIR / "stacked.png")

#: Path to a white, patterned PNG of the logo
WHITE_PATTERN_PNG = str(_DATA_DIR / "white_pattern.png")

#: Path to a grey, patterned PNG of the logo
GREY_PATTERN_PNG = str(_DATA_DIR / "grey_pattern.png")

#: Path to a full-color, patterned PNG of the logo
COLOR_PATTERN_PNG = str(_DATA_DIR / "color_pattern.png")


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


def flag(
    output_filepath: str | bytes | PathLike | None = None,
    size: Sequence[object] | None = None,
):
    """Create a DRC color flag image.

    Parameters
    ----------
    output_filepath : str | bytes | os.PathLike | None
        Optional filepath to save output image.
    size : sequence | None
        Two-item sequence in either order:
        ``[color_widths, height]`` or ``[height, color_widths]``.

    Returns
    -------
    PIL.Image.Image | None
        Returns the image when output_filepath is None; otherwise saves to disk.
    """

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
    watermark_filepath: str | bytes | PathLike = STACKED_LOGO_PNG,
    box: list[float | None] | None = None,
):
    """Watermark a file with the DRC logo, or any other image file."""
    box = [0.0, 0.0, 0.10, None] if box is None else box

    source_image = _Image.open(filepath)
    watermark_image = _Image.open(watermark_filepath)

    if output_filepath is None:
        target_image = source_image
        output_filepath = filepath
    else:
        target_image = source_image.copy()

    source_width = source_image.size[0]
    source_height = source_image.size[1]
    watermark_width = watermark_image.size[0]
    watermark_height = watermark_image.size[1]
    if box[2] is None and box[3] is None:
        resized_watermark_image = watermark_image
    elif box[2] is None and box[3] <= 2.0:
        resized_watermark_image = watermark_image.resize(
            (
                int(watermark_width * (source_height * box[3]) / watermark_height),
                int(source_height * box[3]),
            )
        )
    elif box[3] is None and box[2] <= 2.0:
        resized_watermark_image = watermark_image.resize(
            (
                int(source_width * box[2]),
                int(watermark_height * (source_width * box[2]) / watermark_width),
            )
        )
    else:
        resized_watermark_image = watermark_image.resize(
            (int(source_width * box[2]), int(source_height * box[3]))
        )

    x_position = int(source_width * box[0])
    y_position = int(source_height * box[1])

    target_image.paste(resized_watermark_image, (x_position, y_position))
    target_image.save(output_filepath)
