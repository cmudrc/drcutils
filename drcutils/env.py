from IPython import get_ipython as _get_ipython
from sys import modules as _modules


def is_google_colab() -> bool:
    """Determine whether or not the environment is in Google Colab.

    Returns
    -------
    bool
        True indicates that it is a Google Colab environment.

    """
    return 'google.colab' in _modules


def is_notebook() -> bool:
    """Determine whether or not the environment is in a notebook.

    Returns
    -------
    bool
        True indicates that it is a notebook environment.

    """
    if is_google_colab():
        return True
    else:
        try:
            shell = _get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                return True   # Jupyter notebook or qtconsole
            elif shell == 'TerminalInteractiveShell':
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False      # Probably standard Python interpreter
