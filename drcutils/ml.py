from __future__ import annotations

from netron import serve as _serve
from IPython.display import Javascript as _Javascript
from IPython.core.display import display as _display
from .env import is_notebook
from os import PathLike


def visualize_network(path: str | bytes | PathLike, height: int = 500, port: int = 8000) -> None:

    """Visualize a neural network.

    Visualize a neural network from a path to its saved architecture.
    You can also set the height of visualization (default 500px) and
    which port it is served on (default 8000). The heavy lifting is
    done by netron, which support Netron supports a huge array of file:
    formats ONNX, TensorFlow Lite, Caffe, Keras, Darknet, PaddlePaddle,
    ncnn, MNN, Core ML, RKNN, MXNet, MindSpore Lite, TNN, Barracuda,
    Tengine, CNTK, TensorFlow.js, Caffe2 and UFF.

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
        _serve(path, None, ("localhost", port), False, 0)
        _display(_Javascript("""
        (async ()=>{
            fm = document.createElement('iframe')
            fm.src = await google.colab.kernel.proxyPort(%s)
            fm.width = '95%%'
            fm.height = '%d'
            fm.frameBorder = 0
            document.body.append(fm)
        })();
        """ % (port, height) ))
    else:
        _serve(path, None, ("localhost", port), True, 0)
    
