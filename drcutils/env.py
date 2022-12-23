from IPython import get_ipython as _get_ipython
from sys import modules as _modules


def is_google_colab() -> bool:
    """Returns true if the function is being run in a Google Colab notebook and false if not."""
    return 'google.colab' in _modules


def is_notebook() -> bool:
    """Returns true if the function is being run in a notebook of any sort and false if not."""
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
