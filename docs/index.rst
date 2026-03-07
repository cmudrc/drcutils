drcutils
========

Internal utility toolkit for Design Research Collective lab members.

What This Library Does
----------------------

``drcutils`` provides shared support utilities used across lab projects:
branding assets, figure-export helpers, lightweight file conversion, and runtime
environment detection.

Highlights
----------

- DRC logo, palette, and watermark helpers
- Presentation-ready figure export presets
- CAD and model-visualization wrappers
- Lightweight data-format conversion and runtime checks

Intended Use
------------

This package is intended primarily for internal lab workflows, not as a
general-purpose public framework. It centralizes recurring utility functions so
individual repositories do not duplicate branding and presentation logic.

Integration With The Ecosystem
------------------------------

The Design Research Collective maintains a modular ecosystem of libraries for
research workflows:

- **design-research-agents** for agent execution and trace collection.
- **design-research-problems** for benchmark design tasks and evaluators.
- **design-research-analysis** for analysis pipelines and study outputs.
- **design-research-experiments** for study design and orchestration.
- **drcutils** for shared utility support (branding, visuals, and runtime helpers).

Start Here
----------

- :doc:`quickstart`
- :doc:`installation`
- :doc:`concepts`
- :doc:`typical_workflow`
- :doc:`api`
- `CONTRIBUTING.md <https://github.com/cmudrc/drcutils/blob/main/CONTRIBUTING.md>`_

.. toctree::
   :maxdepth: 2
   :caption: Documentation
   :hidden:

   quickstart
   installation
   concepts
   typical_workflow
   api

.. toctree::
   :maxdepth: 2
   :caption: Development
   :hidden:

   dependencies_and_extras

.. toctree::
   :maxdepth: 2
   :caption: Additional Guides
   :hidden:

   branding
   visualization
   runtime
   cli_standards

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
