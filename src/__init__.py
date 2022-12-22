from __future__ import annotations
# import src.colormaps
# import src.env
# import src.ml
import brand


def import_plotting_stack(alias=True):
    """Import common libraries to support plotting, including:
    - `matplotlib.pyplot`
    - `matplotlib.colors`
    - `pandas`
    - `plotly.express`
    - `plotly.graph_objects`
    - `Pillow`"""
    _gimme(
        matplotlib__dot__pyplot=["matplotlib.pyplot", "plt"][alias],
        matplotlib__dot__colors=["matplotlib.colors", "mpc"][alias],
        pandas=["pandas", "pd"][alias],
        plotly__dot__express=["plotly.express", "px"][alias],
        plotly__dot__graph_objects=["plotly.graph_objects", "go"][alias],
        Pillow=["Pillow", "PIL"][alias],
    )


def import_stats_stack(alias=True):
    """Import common libraries to support statistical testing, including:
    - `numpy`
    - `pandas`
    - `scipy.stats`
    - `statsmodels`"""
    _gimme(
        numpy=["numpy", "np"][alias],
        pandas=["pandas", "pd"][alias],
        scipy__dot__stats=["scipy.stats", "ss"][alias],
        statsmodels=["statsmodels", "sm"][alias]
    )


def import_hf_stack(alias=True):
    """Import common libraries to support statistical testing, including:
    - `numpy`
    - `pandas`
    - `huggingface_hub`
    - `datasets`
    - `gradio`"""
    _gimme(
        numpy=["numpy", "np"][alias],
        pandas=["pandas", "pd"][alias],
        huggingface_hub=["huggingface_hub", "hub"][alias],
        datasets=["datasets", "datasets"][alias],
        gradio=["gradio", "gr"][alias],
    )


def _gimme(**kwargs):
    """Imports libraries programmatically"""

    from importlib import import_module

    modules = dict()
    for keyword in kwargs.keys():
        modules[keyword.replace("__dot__", ".")] = kwargs[keyword]

    for module_name in modules.keys():
        print(f'Importing {module_name.replace("__dot__", ".")} as {modules[module_name]}... ', end="")
        try:
            globals()[modules[module_name]] = import_module(module_name)
            print('Done!')
        except ModuleNotFoundError:
            print(":(")
            raise ModuleNotFoundError(
                f'Could not import {module_name.replace("__dot__", ".")}. It may not be installed.')



