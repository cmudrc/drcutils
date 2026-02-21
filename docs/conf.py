import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

autodoc_mock_imports = [
    "numpy",
    "stl",
    "pandas",
    "matplotlib",
    "plotly",
    "netron",
    "PIL",
    "IPython",
]

project = "drcutils"
copyright = "2026, The Design Research Collective"
author = "The Design Research Collective"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autosummary_generate = True
autodoc_typehints = "none"
suppress_warnings = ["ref.class"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

if os.environ.get("READTHEDOCS") == "True":
    html_theme = "sphinx_rtd_theme"
else:
    try:
        import sphinx_rtd_theme  # noqa: F401

        html_theme = "sphinx_rtd_theme"
    except ImportError:
        html_theme = "alabaster"

html_static_path = ["_static"]
