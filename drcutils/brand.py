from __future__ import annotations
import pkg_resources
from os import PathLike
from PIL import Image as _Image
import matplotlib.colors as _mpc
from numpy import array as _array, uint8 as _uint8
# from PIL.Image import open as _open, Image as _Image
from os.path import splitext as _splitext


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
    rgb_colors = [_array(_mpc.to_rgb(c)) for c in COLORS]
    width = size[0] if type(size[0]) == "int" else size[1]
    colors = size[1] if type(size[1]) == "list" else size[0]

    color_list = []
    for idx, color_width in enumerate(colors):
        color_list = color_list + list([rgb_colors[idx]]) * color_width

    flag_image = _Image.fromarray(_uint8(_array([color_list] * width) * 255), mode="RGBA")

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


def convert_image(convert_from: str | bytes | PathLike, convert_to: str | bytes | PathLike,
                  from_kwargs: dict = None, to_kwargs: dict = None):

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
        ".png": _Image.open,
        ".jpg": _Image.open,
        ".jpeg": _Image.open,
        ".eps": _Image.open,
        ".bmp": _Image.open,
    }

    _to_image_extensions = {
        ".png": _Image.Image.save,
        ".jpg": _Image.Image.save,
        ".jpeg": _Image.Image.save,
        ".eps": _Image.Image.save,
        ".bmp": _Image.Image.save,
    }

    from_ext = _splitext(convert_from)[1]
    to_ext = _splitext(convert_to)[1]

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

