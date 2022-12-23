from __future__ import annotations
from PIL import Image as _Image


def convert(thing_to_convert_from: str, thing_to_convert_to: str, filetype="auto"):
    """Convert between lots of commonn file formats."""
    if filetype is "auto":
        filetype = _what_kind_of_file_is_this(thing_to_convert_from)

    if filetype == "image":
        img = _Image.open(thing_to_convert_from)
        img.save(thing_to_convert_to)
    else:
        raise SyntaxError()


def _what_kind_of_file_is_this(filename: str) -> str | None:
    """Returns the filetype if known, otherwise None."""
    if is_it_an_image(filename):
        return "image"
    elif is_it_a_model(filename):
        return "model"
    elif is_it_data(filename):
        return "data"
    else:
        return None


def is_it_an_image(filename: str) -> bool:
    """If the filename is an image, returns True."""
    if filename.lower().endswith(".png") or \
            filename.lower().endswith(".jpg") or \
            filename.lower().endswith(".jpeg") or \
            filename.lower().endswith(".eps") or \
            filename.lower().endswith(".bmp"):
        return True
    else:
        return False


def is_it_a_model(filename: str) -> bool:
    """If the filename is a model, returns True."""
    if filename.lower().endswith(".pb") or \
            filename.lower().endswith(".mlmodel") or \
            filename.lower().endswith(".onnx") or \
            filename.lower().endswith(".pkl"):
        return True
    else:
        return False


def is_it_data(filename: str) -> bool:
    """If the filename is a model, returns True."""
    if filename.lower().endswith(".csv") or \
            filename.lower().endswith(".hdf5") or \
            filename.lower().endswith(".h5") or \
            filename.lower().endswith(".json") or \
            filename.lower().endswith(".parquet"):
        return True
    else:
        return False
