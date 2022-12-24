# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

autodoc_mock_imports = [
            "IPython",
            "matplotlib",
            "netron",
            "numpy",
            "numpy-stl",
            "Pillow",
            "plotly",
            "svgpathtools",
    ]

# Add to path for autobuild
sys.path.insert(0, os.path.abspath('..'))

project = 'drcutils'
copyright = '2022, The Design Research Collective'
author = 'The Design Research Collective'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'recommonmark']
source_suffix = [".rst"]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


import pathlib

# The readme that already exists
readme_path = pathlib.Path(__file__).parent.resolve().parent / "README.md"
# We copy a modified version here
readme_target = pathlib.Path(__file__).parent / "readme.rst"

with readme_target.open("w") as outf:
    # Change the title to "Readme"
    outf.write(
        "\n".join(
            [
                "Readme",
                "=======================\n",
            ]
        )
    )
    lines = []
    for line in readme_path.read_text().split("\n"):
        if line.startswith("# "):
            # Skip title, because we now use "Readme"
            # Could also simply exclude first line for the same effect
            continue
        lines.append(line)
    outf.write("\n".join(lines))