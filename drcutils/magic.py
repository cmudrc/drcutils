from __future__ import annotations

from os import PathLike
from os.path import splitext as _splitext

import pandas as _pandas
from PIL.Image import Image as _Image, open as _open


def _get_data_extensions():
    _from_data_extensions = {
        ".png": _open,
        ".jpg": _open,
        ".jpeg": _open,
        ".eps": _open,
        ".bmp": _open,
        ".csv": _pandas.read_csv,
        ".hdf5": _pandas.read_hdf,
        ".h5": _pandas.read_hdf,
        ".json": _pandas.read_json,
        ".xml": _pandas.read_xml,
        ".parquet": _pandas.read_parquet,
        ".xls": _pandas.read_excel,
        ".xlsx": _pandas.read_excel,
        ".feather": _pandas.read_feather,
        ".dta": _pandas.read_stata,
        ".xpt": _pandas.read_sas,
        ".sas7bdat": _pandas.read_sas,
        ".sav": _pandas.read_spss,
        ".zsav": _pandas.read_spss,
        ".pkl": _pandas.read_pickle,
    }

    _to_data_extensions = {
        ".png": _Image.save,
        ".jpg": _Image.save,
        ".jpeg": _Image.save,
        ".eps": _Image.save,
        ".bmp": _Image.save,
        ".csv": _pandas.DataFrame.to_csv,
        ".hdf5": _pandas.DataFrame.to_hdf,
        ".h5": _pandas.DataFrame.to_hdf,
        ".json": _pandas.DataFrame.to_json,
        ".xml": _pandas.DataFrame.to_xml,
        ".parquet": _pandas.DataFrame.to_parquet,
        ".xls": _pandas.DataFrame.to_excel,
        ".xlsx": _pandas.DataFrame.to_excel,
        ".feather": _pandas.DataFrame.to_feather,
        ".dta": _pandas.DataFrame.to_stata,
        ".pkl": _pandas.DataFrame.to_pickle,
    }

    return _to_data_extensions, _from_data_extensions


def _convertible(from_ext: str, to_ext: str) -> bool:
    """Check if a file conversion is possible."""
    _to_data_extensions, _from_data_extensions = _get_data_extensions()
    to_fun = str(_to_data_extensions[to_ext])
    from_fun = str(_from_data_extensions[from_ext])
    if "to_" in to_fun and "read_" in from_fun:
        return True
    if "Image.save" in to_fun and "open" in from_fun:
        return True
    if ".pt" in from_ext and "onnx" in to_ext:
        return True
    return False


def convert(
    thing_to_convert_from: str | bytes | PathLike,
    thing_to_convert_to: str | bytes | PathLike,
    from_kwargs: dict | None = None,
    to_kwargs: dict | None = None,
):
    """Convert stuff to other stuff. Works for images and data files."""
    from_kwargs = {} if from_kwargs is None else from_kwargs
    to_kwargs = {} if to_kwargs is None else to_kwargs

    _to_data_extensions, _from_data_extensions = _get_data_extensions()
    from_ext = _splitext(str(thing_to_convert_from))[1].lower()
    to_ext = _splitext(str(thing_to_convert_to))[1].lower()

    if from_ext not in _from_data_extensions:
        supported_from = ", ".join(sorted(_from_data_extensions.keys()))
        raise ValueError(
            f"Files with extension {from_ext} cannot be opened. Supported: {supported_from}"
        )

    if to_ext not in _to_data_extensions:
        supported_to = ", ".join(sorted(_to_data_extensions.keys()))
        raise ValueError(
            f"Files with extension {to_ext} cannot be written. Supported: {supported_to}"
        )

    if not _convertible(from_ext, to_ext):
        raise ValueError(
            f"Files with extension {from_ext} cannot be converted to extension {to_ext}."
        )

    _to_data_extensions[to_ext](
        _from_data_extensions[from_ext](
            thing_to_convert_from,
            **from_kwargs,
        ),
        thing_to_convert_to,
        **to_kwargs,
    )
