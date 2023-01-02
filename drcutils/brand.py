from __future__ import annotations

import os
import typing

import PIL
import PIL as _PIL
import matplotlib.colors as _matplotlib_colors
import matplotlib.pyplot as _matplotlib_pyplot
import numpy as _numpy
import pkg_resources

#: The colors of the DRC brand
COLORS: typing.Final[typing.List[str]] = [
    "#000000",
    "#1A4C49",
    "#4C8687",
    "#58B7BB",
    "#EA8534",
    "#DF5227"
]

#: Path to an SVG of logo
LOGO_ONLY_SVG: typing.Final[str] = pkg_resources.resource_filename('drcutils', 'data/logo.svg')

#: Path to a PNG of logo
LOGO_ONLY_PNG: typing.Final[str] = pkg_resources.resource_filename('drcutils', 'data/logo.png')

#: Path to an STL of logo
LOGO_ONLY_STL: typing.Final[str] = pkg_resources.resource_filename('drcutils', 'data/logo.stl')

#: Path to a PNG of the horizontal logo
HORIZONTAL_LOGO_PNG: typing.Final[str] = pkg_resources.resource_filename('drcutils', 'data/horizontal.png')

#: Path to a PNG of the stacked logo
STACKED_LOGO_PNG: typing.Final[str] = pkg_resources.resource_filename('drcutils', 'data/stacked.png')

#: Path to a white, patterned PNG of the logo
WHITE_PATTERN_PNG: typing.Final[str] = pkg_resources.resource_filename('drcutils', 'data/white_pattern.png')

#: Path to a grey, patterned PNG of the logo
GREY_PATTERN_PNG: typing.Final[str] = pkg_resources.resource_filename('drcutils', 'data/grey_pattern.png')

#: Path to a full-color, patterned PNG of the logo
COLOR_PATTERN_PNG: typing.Final[str] = pkg_resources.resource_filename('drcutils', 'data/color_pattern.png')

#: Path to a DRC-brand matplotlib style file
DRC_MPLSTYLE: typing.Final[str] = pkg_resources.resource_filename('drcutils', 'data/drc.mplstyle')


def make_flag(output_filepath: typing.Optional[str | bytes | os.PathLike] = None,
              size: typing.Optional[typing.Tuple[int, int]] = None,
              stripe_thickness: typing.Optional[typing.Sequence[float]] = None,
              mode: typing.Literal["dark", "light"] = "dark") -> typing.Optional[PIL.Image]:
    """
    Make a DRC flag.

    THis function creates a layout of the DRC colors. This pattern is suitable for social media
    headers, presentations backgrounds, document footers, etc.

    Parameters
    ----------
    output_filepath : Optional[str | bytes | os.PathLike]
        The filepath to save the flag to, if given.
    size: Optional[Tuple[int, int]]
        The image size in pixels as a width-height tuple.
    stripe_thickness: Optional[Sequence[float]]
        The thickness of each of the color stripes.
    mode: Literal["dark", "light"]
        If "dark", then black is the neutral color used in the flag. If "light, white is the neutral color.

    Returns
    -------
    None | PIL.Image
        If `output_filepath` is not given, then output a _PIL.Image object. If `output_filepath` is given, no output.

    """

    # Handle default values
    if size is None:
        size = (1500, 500)
    if stripe_thickness is None:
        stripe_thickness = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]

    # Set stripe thickness to actual pixels
    stripe_thickness = [int(size[0] * t) for t in stripe_thickness]

    rgb_colors = [_numpy.array(_matplotlib_colors.to_rgb(c)) for c in COLORS]
    if mode == "light":
        rgb_colors = [_numpy.array([1.0, 1.0, 1.0]), rgb_colors[3], rgb_colors[2], rgb_colors[1], rgb_colors[5],
                      rgb_colors[4]]

    color_list = []
    for idx, color_width in enumerate(stripe_thickness):
        color_list = color_list + list([rgb_colors[idx]]) * color_width

    flag_image = _PIL.Image.fromarray(_numpy.uint8(_numpy.array([color_list] * size[1]) * 255)).convert("RGBA")

    if output_filepath is None:
        return flag_image
    else:
        flag_image.save(output_filepath)


def watermark(filepath: str | bytes | os.PathLike, output_filepath: str | bytes | os.PathLike = None,
              watermark_filepath: str | bytes | os.PathLike = None,
              box: [float, float, float | None, float | None] = None):
    """A function to watermark files with the DRC logo, or any other image file."""

    if watermark_filepath is None:
        watermark_filepath = STACKED_LOGO_PNG
    if box is None:
        box = [0.0, 0.0, 0.10, None]
    source_image = _PIL.Image.open(filepath)
    watermark_image = _PIL.Image.open(watermark_filepath)

    target_image = source_image.copy()

    # Calculate target size in pixels
    source_width = source_image.size[0]
    source_height = source_image.size[1]
    watermark_width = watermark_image.size[0]
    watermark_height = watermark_image.size[1]
    if box[2] is None and box[3] is None:
        resized_watermark_image = watermark_image
    elif box[2] is None and box[3] <= 2.0:
        resized_watermark_image = watermark_image.resize(
            (int(watermark_width * (source_height * box[3]) / watermark_height), int(source_height * box[3])))
    elif box[3] is None and box[2] <= 2.0:
        resized_watermark_image = watermark_image.resize(
            (int(source_width * box[2]), int(watermark_height * (source_width * box[2]) / watermark_width)))
    else:
        resized_watermark_image = watermark_image.resize((int(source_width * box[2]), int(source_height * box[3])))

    # Calculate target position in pixels
    x_position = int(source_width * box[0])
    y_position = int(source_height * box[1])

    # Position and add the image
    target_image.paste(resized_watermark_image, (x_position, y_position))

    # Save the image or return it
    if output_filepath is None:
        return target_image
    else:
        target_image.save(output_filepath)


def convert_image(convert_from: str | bytes | os.PathLike, convert_to: str | bytes | os.PathLike,
                  from_kwargs: typing.Optional[typing.Dict] = None,
                  to_kwargs: typing.Optional[typing.Dict] = None) -> None:
    """Convert between different image formats.

    This function is essentially a thing wrapper around pandas, and uses that library as a backend for
    all conversions. That being said, it is pretty robust, and can handle conversions from (.png, .jpg, .jpeg, .eps,
    .bmp) and to (.png, .jpg, .jpeg, .eps, .bmp) a variety of filetypes.

    Parameters
    ----------
    convert_from : str | bytes | os.PathLike
        A path to the file to convert from.
    convert_to : str | bytes | os.PathLike
        A path to the file to convert to.
    from_kwargs : dict
        A dictionary of any keyword arguments for the function used to load the file.
    to_kwargs : dict
        A dictionary of any keyword arguments for the function used to write the file.

    Returns
    -------
    None
        Simple writes a new file.

    """

    if to_kwargs is None:
        to_kwargs = {}
    if from_kwargs is None:
        from_kwargs = {}

    _from_image_extensions = {
        ".png": _PIL.Image.open,
        ".jpg": _PIL.Image.open,
        ".jpeg": _PIL.Image.open,
        ".eps": _PIL.Image.open,
        ".bmp": _PIL.Image.open,
    }

    _to_image_extensions = {
        ".png": _PIL.Image.Image.save,
        ".jpg": _PIL.Image.Image.save,
        ".jpeg": _PIL.Image.Image.save,
        ".eps": _PIL.Image.Image.save,
        ".bmp": _PIL.Image.Image.save,
    }

    from_ext = os.path.splitext(convert_from)[1]
    to_ext = os.path.splitext(convert_to)[1]

    if from_ext in _from_image_extensions.keys():
        if to_ext in _to_image_extensions.keys():
            _to_image_extensions[to_ext](
                _from_image_extensions[from_ext](
                    convert_from,
                    **from_kwargs
                ),
                convert_to,
                **to_kwargs
            )
        else:
            raise ValueError(f"Files with extension {to_ext} cannot be written.")
    else:
        raise ValueError(f"Files with extension {from_ext} cannot be opened.")


def drc_style() -> None:
    """The custom DRC matplotlib style.

    """
    return _matplotlib_pyplot.style.context(DRC_MPLSTYLE)


del PIL
