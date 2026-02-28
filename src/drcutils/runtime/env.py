"""Environment detection helpers for notebook and Colab runtimes."""

from sys import modules as _modules

from IPython import get_ipython as _get_ipython


def is_google_colab() -> bool:
    """Determine whether or not the environment is in Google Colab.

    Returns:
        ``True`` when running in Google Colab.
    """
    return "google.colab" in _modules


def is_notebook() -> bool:
    """Determine whether or not the environment is in a notebook.

    Returns:
        ``True`` when running in a notebook runtime.
    """
    if is_google_colab():
        return True
    else:
        try:
            shell = _get_ipython().__class__.__name__
            if shell == "ZMQInteractiveShell":
                return True  # Jupyter notebook or qtconsole
            elif shell == "TerminalInteractiveShell":
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False  # Probably standard Python interpreter
