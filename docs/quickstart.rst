Quickstart
==========

This example shows the shortest meaningful path through ``drcutils``.

1. Install
----------

.. code-block:: bash

   pip install drcutils

Or install from source:

.. code-block:: bash

   git clone https://github.com/cmudrc/drcutils.git
   cd drcutils
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   pip install -e .

2. Minimal Runnable Example
---------------------------

.. code-block:: python

   import matplotlib.pyplot as plt

   from drcutils import convert, export_figure, is_notebook

   convert("inputs/study.csv", "artifacts/study.json")

   fig, ax = plt.subplots()
   ax.plot([0, 1, 2], [0, 1, 4])
   result = export_figure(fig, "artifacts/figures/main_result")

   print(is_notebook())
   print(result["files"])

3. What Happened
----------------

You converted a data artifact, exported a publication-style figure, and checked
runtime context. This is the most common internal-lab usage pattern.

4. Where To Go Next
-------------------

- :doc:`concepts`
- :doc:`typical_workflow`
- :doc:`branding`
- :doc:`visualization`

Ecosystem Note
--------------

In typical lab workflows, ``drcutils`` is the support layer used alongside
``design-research-agents``, ``design-research-problems``,
``design-research-experiments``, and ``design-research-analysis``.
