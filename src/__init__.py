from __future__ import annotations


def is_colab() -> bool:
    """Returns true if the function is being run in a Google Colab notebook and false if not."""
    import sys
    return 'google.colab' in sys.modules


def is_notebook() -> bool:
    """Returns true if the function is being run in a notebook of any sort and false if not."""
    if is_colab():
        return True
    else:
        try:
            shell = get_ipython().__class__.__name__
            print(shell)
            if shell == 'ZMQInteractiveShell':
                return True   # Jupyter notebook or qtconsole
            elif shell == 'TerminalInteractiveShell':
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False      # Probably standard Python interpreter


def gimme(numpy: bool | str = "np",
          pandas: bool | str = "pd",
          matplotlib_pyplot: bool | str = "plt",
          matplotlib_colors: bool | str = "mpc",
          pillow: bool | str = "PIL",
          datasets: bool | str = "data",
          huggingface_hub: bool | str = "hub",
          gradio: bool | str = "gr",
          plotly_express: bool | str = "px",
          plotly_graph_objects: bool | str = "go",
          be_nice = False,
          **kwargs):
    """Imports libraries programmatically"""

    import importlib
    modules = {
        "numpy": numpy,
        "pandas": pandas,
        "Pillow": pillow,
        "matplotlib.pyplot": matplotlib_pyplot,
        "matplotlib.colors": matplotlib_colors,
        "datasets": datasets,
        "huggingface_hub": huggingface_hub,
        "gradio": gradio,
        "plotly_express": plotly_express,
        "plotly_graph_objects": plotly_graph_objects,
    }
    modules.update(kwargs)
    for module_name in modules.keys():
        if modules[module_name]:
            try:
                globals()[modules[module_name]] = importlib.import_module(module_name)
            except ModuleNotFoundError:
                if be_nice:
                    raise ImportWarning(f'Could not import {module_name}. It may not be installed.')
                else:
                    ModuleNotFoundError(f'Could not import {module_name}. It may not be installed.')