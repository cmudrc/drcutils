from __future__ import annotations

import os.path
import typing

import IPython.core.display as _ipycoredis
import IPython.display as _ipydis
import netron as _netron
import pandas as _pandas

from .env import is_notebook


def convert_data(convert_from: str | bytes | os.PathLike, convert_to: str | bytes | os.PathLike,
                 from_kwargs: typing.Optional[typing.Dict] = None,
                 to_kwargs: typing.Optional[typing.Dict] = None) -> None:
    """Convert between different data formats.

    This function is essentially a thing wrapper around pandas, and uses that library as a backend for
    all conversions. That being said, it is pretty robust, and can handle conversions from (.csv, .hdf5, .h5, .json,
    .xml, .parquet, .xls, .xlsx, .dta, .feather, .xpt, .sas7bdat, .sav, .zsav, and .pkl) and to (.csv, .hdf5, .h5, .json,
    .xml, .parquet, .xls, .xlsx, .feather, .dta, and .pkl, but NOT .xpt, .sas7bdat, .sav, or .zsav) a variety of filetypes.

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

    # Replace with mutable values
    if to_kwargs is None:
        to_kwargs = {}
    if from_kwargs is None:
        from_kwargs = {}

    _from_data_extensions = {
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

    # Figure out what functions to use
    from_ext = os.path.splitext(convert_from)[1]
    to_ext = os.path.splitext(convert_to)[1]

    if from_ext in _from_data_extensions.keys():
        if to_ext in _to_data_extensions.keys():
            _to_data_extensions[to_ext](
                _from_data_extensions[from_ext](
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


def visualize_network(path: str | bytes | os.PathLike, height: int = 500, port: int = 8000) -> None:
    """Visualize a neural network.

    Visualize a neural network from a path to its saved architecture. You can also set the height of visualization
    (default 500px) and which port it is served on (default 8000). The heavy lifting is done by netron, which support
    supports a huge array of file formats: ONNX, TensorFlow Lite, Caffe, Keras, Darknet, PaddlePaddle, ncnn, MNN, Core
    ML, RKNN, MXNet, MindSpore Lite, TNN, Barracuda, Tengine, CNTK, TensorFlow.js, Caffe2 and UFF.

    Parameters
    ----------
    path : str | bytes | os.PathLike
        A filepath to the saved neural network
    height: int
        The height of the iframe visualization in pixels [optional; default = 500]
    port: int
        The port on which the visualization is served [optional; default = 8000]

    Returns
    -------
    None
        Opens the visualization in an iframe (if in a notebook) or otherwise in a browser window.

    """

    if is_notebook():
        _netron.serve(path, None, ("localhost", port), False, 0)
        _ipycoredis.display(_ipydis.Javascript("""
        (async ()=>{
            fm = document.createElement('iframe')
            fm.src = await google.colab.kernel.proxyPort(%s)
            fm.width = '95%%'
            fm.height = '%d'
            fm.frameBorder = 0
            document.body.append(fm)
        })();
        """ % (port, height)))
    else:
        _netron.serve(path, None, ("localhost", port), True, 0)
