from __future__ import annotations
import pkg_resources
from os import PathLike
from PIL import Image as _Image
import matplotlib.colors as _mpc
import numpy

#: The colors of the DRC brand
COLORS = [
    "#000000",
    "#1A4C49",
    "#4C8687",
    "#58B7BB",
    "#EA8534",
    "#DF5227"
]

#: Path to an SVG of logo
LOGO_ONLY_SVG = pkg_resources.resource_filename('drcutils', 'data/logo.svg')

#: Path to a PNG of logo
LOGO_ONLY_PNG = pkg_resources.resource_filename('drcutils', 'data/logo.png')

#: Path to an STL of logo
LOGO_ONLY_STL = pkg_resources.resource_filename('drcutils', 'data/logo.stl')

#: Path to a PNG of the horizontal logo
HORIZONTAL_LOGO_PNG = pkg_resources.resource_filename('drcutils', 'data/horizontal.png')

#: Path to a PNG of the stacked logo
STACKED_LOGO_PNG = pkg_resources.resource_filename('drcutils', 'data/stacked.png')

#: Path to a white, patterned PNG of the logo
WHITE_PATTERN_PNG = pkg_resources.resource_filename('drcutils', 'data/white_pattern.png')

#: Path to a grey, patterned PNG of the logo
GREY_PATTERN_PNG = pkg_resources.resource_filename('drcutils', 'data/grey_pattern.png')

#: Path to a full-color, patterned PNG of the logo
COLOR_PATTERN_PNG = pkg_resources.resource_filename('drcutils', 'data/color_pattern.png')


def flag(output_filepath: str | bytes | PathLike = None, size=None):
    if size is None:
        size = [[50, 10, 10, 10, 10, 10], 100]
    rgb_colors = [numpy.array(_mpc.to_rgb(c)) for c in COLORS]
    width = size[0] if type(size[0]) == "int" else size[1]
    colors = size[1] if type(size[1]) == "list" else size[0]

    color_list = []
    for idx, color_width in enumerate(colors):
        color_list = color_list + list([rgb_colors[idx]]) * color_width

    flag_image = _Image.fromarray(numpy.uint8(numpy.array([color_list] * width) * 255), mode="RGBA")

    if output_filepath is None:
        return flag_image
    else:
        flag_image.save(output_filepath)


def watermark(filepath: str | bytes | PathLike, output_filepath: str | bytes | PathLike = None,
              watermark_filepath: str | bytes | PathLike = STACKED_LOGO_PNG,
              box: [float, float, float | None, float | None] = [0.0, 0.0, 0.10, None]):
    """A function to watermark files with the DRC logo, or any other image file."""

    source_image = _Image.open(filepath)
    watermark_image = _Image.open(watermark_filepath)

    if output_filepath is None:
        target_image = source_image
        output_filepath = filepath
    else:
        target_image = source_image.copy()

    # Calculate target size in pixels
    source_width = source_image.size[0]
    source_height = source_image.size[1]
    watermark_width = watermark_image.size[0]
    watermark_height = watermark_image.size[1]
    if box[2] is None and box[3] is None:
        resized_watermark_image = watermark_image
    elif box[2] is None and box[3] <= 2.0:
        resized_watermark_image = watermark_image.resize((int(watermark_width * (source_height * box[3]) / watermark_height), int(source_height*box[3])))
    elif box[3] is None and box[2] <= 2.0:
        resized_watermark_image = watermark_image.resize((int(source_width*box[2]), int(watermark_height * (source_width * box[2]) / watermark_width)))
    else:
        resized_watermark_image = watermark_image.resize((int(source_width*box[2]), int(source_height*box[3])))

    # Calculate target position in pixels
    x_position = int(source_width*box[0])
    y_position = int(source_height*box[1])

    # Position and add the image
    target_image.paste(resized_watermark_image, (x_position, y_position))

    # Save the image
    target_image.save(output_filepath)
