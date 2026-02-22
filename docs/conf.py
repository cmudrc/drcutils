"""Sphinx configuration for drcutils docs."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

autoclass_content = "both"

project = "drcutils"
copyright = "2026, The Design Research Collective"
author = "The Design Research Collective"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_param = True
napoleon_use_rtype = False

autodoc_typehints = "none"
autosummary_generate = True
autosummary_imported_members = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_mock_imports = [
    "numpy",
    "stl",
    "pandas",
    "matplotlib",
    "netron",
    "PIL",
    "IPython",
]

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
html_logo = "drc.png"
html_theme_options = {
    "logo_only": True,
}
