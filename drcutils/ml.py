from __future__ import annotations

from os import PathLike

from IPython.display import Javascript as _Javascript, display as _display
from netron import serve as _serve

from .env import is_google_colab, is_notebook


def visualize_network(path: str | bytes | PathLike, height: int = 500, port: int = 8000) -> None:
    """Visualize a neural network with Netron.

    Parameters
    ----------
    path : str | bytes | os.PathLike
        A filepath to the saved neural network.
    height: int
        The height of the iframe visualization in pixels.
    port: int
        The port on which the visualization is served.

    Returns
    -------
    None
        Opens the visualization in an iframe (if in a notebook) or otherwise in a browser window.
    """

    if is_notebook():
        _serve(path, None, ("localhost", port), False, 0)
        if is_google_colab():
            _display(
                _Javascript(
                    """
            (async ()=>{
                const fm = document.createElement('iframe');
                fm.src = await google.colab.kernel.proxyPort(%s);
                fm.width = '95%%';
                fm.height = '%d';
                fm.frameBorder = 0;
                document.body.append(fm);
            })();
            """
                    % (port, height)
                )
            )
        else:
            _display(
                _Javascript(
                    """
            (()=>{
                const fm = document.createElement('iframe');
                fm.src = 'http://localhost:%s';
                fm.width = '95%%';
                fm.height = '%d';
                fm.frameBorder = 0;
                document.body.append(fm);
            })();
            """
                    % (port, height)
                )
            )
    else:
        _serve(path, None, ("localhost", port), True, 0)
