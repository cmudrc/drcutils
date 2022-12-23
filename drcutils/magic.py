from __future__ import annotations
from PIL import Image as _Image


def convert(thing_to_convert_from: str, thing_to_convert_to: str, filetype="auto"):
    """Convert between lots of commonn file formats."""
    if filetype is "auto":
        filetype = _what_type_is_this_file(thing_to_convert_from)

    if filetype == "image":
        img = _Image.open(thing_to_convert_from)
        img.save(thing_to_convert_to)


def _what_type_is_this_file(filename: str) -> str | None:
    """Returns the filetype if known, otherwise None."""
    if is_it_an_image(filename):
        return "image"
    else:
        return None


def is_it_an_image(filename: str) -> bool:
    """If the pilename is an image, returns True."""
    if filename.lower().endswith("png") or \
            filename.lower().endswith("jpg") or \
            filename.lower().endswith("jpeg") or \
            filename.lower().endswith("eps") or \
            filename.lower().endswith("bmp"):
        return True
    else:
        return False
