from __future__ import annotations

import os
import typing

import IPython.display as _ipython_display
import netron as _netron
import pandas as _pandas
import sklearn.decomposition as _sklearn_decomposition
import sklearn.manifold as _sklearn_manifold

from .env import is_notebook as _is_notebook


class Embedding:
    algorithm_info = {
        "pca": {
            "proper_name": "PCA",
            "model": _sklearn_decomposition.PCA,
            "reusable": True,
            "reversible": True,
        },
        "kernelpca": {
            "proper_name": "Kernel PCA",
            "model": _sklearn_decomposition.KernelPCA,
            "reusable": True,
            "reversible": True,
        },
        "sparsepca": {
            "proper_name": "Sparse PCA",
            "model": _sklearn_decomposition.SparsePCA,
            "reusable": True,
            "reversible": True,
        },
        "truncatedsvd": {
            "proper_name": "Truncated SVD",
            "model": _sklearn_decomposition.TruncatedSVD,
            "reusable": True,
            "reversible": True,
        },
        "tsne": {
            "proper_name": "t-SNE",
            "model": _sklearn_manifold.TSNE,
            "reusable": False,
            "reversible": False,
        },
        "isomap": {
            "proper_name": "Isometric Mapping",
            "model": _sklearn_manifold.Isomap,
            "reusable": True,
            "reversible": False,
        },
        "lle": {
            "proper_name": "Locally Linear Embedding",
            "model": _sklearn_manifold.LocallyLinearEmbedding,
            "reusable": True,
            "reversible": False,
        },
        "mds": {
            "proper_name": "Multidimensional Scaling",
            "model": _sklearn_manifold.MDS,
            "reusable": False,
            "reversible": False,
        }
    }

    def __init__(self, n_components: int = 2, algorithm: typing.Literal["pca", "sparsepca", "kernelpca", "truncatedsvd", "tsne", "isomap", "lle", "mds"] = "pca", **kwargs):
        self.algorithm_name = algorithm
        self.model = Embedding.algorithm_info[self.algorithm_name]["model"](n_components=n_components, **kwargs)

    def fit(self, X):
        if self.reusable:
            self.model.fit(X)
        else:
            raise ValueError(f"The {self.proper_name} algorithm does not train a reusable model, so please use the `fit_transform` "
                             "function instead.")

    def transform(self, X):
        if self.reusable:
            return self.model.transform(X)
        else:
            raise ValueError(f"The {self.proper_name} algorithm does not train a reusable model, so please use the `fit_transform` "
                             "function instead.")

    def fit_transform(self, X):
        return self.model.fit_transform(X)

    def inverse_transform(self, X):
        if self.reversible:
            return self.model.inverse_transform(X)
        else:
            raise ValueError(f"The {self.proper_name} algorithm is not reversible, so please consider using a different algorithm.")

    @property
    def proper_name(self):
        return Embedding.algorithm_info[self.algorithm_name]['proper_name']

    @property
    def reusable(self):
        return Embedding.algorithm_info[self.algorithm_name]['reusable']

    @property
    def reversible(self):
        return Embedding.algorithm_info[self.algorithm_name]['reversible']


def convert_data(convert_from: str | bytes | os.PathLike, convert_to: str | bytes | os.PathLike,
                 from_kwargs: typing.Optional[typing.Dict[str, typing.Any]] = None,
                 to_kwargs: typing.Optional[typing.Dict[str, typing.Any]] = None) -> None:
    """
    Convert between different data formats.

    This function is essentially a thing wrapper around pandas, and uses that library as a backend for
    all conversions. That being said, it is pretty robust, and can handle conversions from (.csv, .hdf5, .h5, .json,
    .xml, .parquet, .xls, .xlsx, .dta, .feather, .xpt, .sas7bdat, .sav, .zsav, and .pkl) and to (.csv, .hdf5, .h5,
    .json, .xml, .parquet, .xls, .xlsx, .feather, .dta, and .pkl, but NOT .xpt, .sas7bdat, .sav, or .zsav) a variety of
    filetypes.

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

    # Dict of functions used to read into pandas
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

    # Dict of functions used to write out of pandas
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


def visualize_network(path: str | bytes | os.PathLike, height: typing.Optional[int] = 500,
                      port: typing.Optional[int] = 8000) -> None:
    """
    Visualize a neural network.

    Visualize a neural network from a path to its saved architecture. You can also set the height of visualization
    (default 500px) and which port it is served on (default 8000). The heavy lifting is done by netron, which support
    supports a huge array of file formats: ONNX, TensorFlow Lite, Caffe, Keras, Darknet, PaddlePaddle, ncnn, MNN, Core
    ML, RKNN, MXNet, MindSpore Lite, TNN, Barracuda, Tengine, CNTK, TensorFlow.js, Caffe2 and UFF.

    Parameters
    ----------
    path : str | bytes | os.PathLike
        A filepath to the saved neural network
    height: Optional[int]
        The height of the iframe visualization in pixels [optional; default = 500]
    port: Optional[int]
        The port on which the visualization is served [optional; default = 8000]

    Returns
    -------
    None
        Opens the visualization in an iframe (if in a notebook) or otherwise in a browser window.

    """

    # If in a notebook environment, display using IPython. Otherwise, serve it and open up a new window.
    if _is_notebook():
        _netron.serve(path, bytes(), ("localhost", port), False, 0)
        _ipython_display.display(_ipython_display.Javascript("""
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
        _netron.serve(path, bytes(), ("localhost", port), True, 0)

