Paper Figure Exporter
=====================

Overview
--------

Use ``drcutils.viz.export_figure`` to export Matplotlib figures with
publication-friendly presets and consistent output naming.

Quick Start
-----------

.. code-block:: python

   import matplotlib.pyplot as plt
   from drcutils.viz import export_figure

   fig, ax = plt.subplots()
   ax.plot([0, 1, 2], [0, 1, 4], label="trend")
   ax.set_xlabel("Time")
   ax.set_ylabel("Score")
   ax.legend()

   result = export_figure(
       fig,
       "artifacts/figures/main_result",
       targets=["one_col", "slide_16x9"],
       formats=["pdf", "png"],
       dpi=300,
   )

   print(result["files"])
   print(result["warnings"])

API Reference
-------------

.. automodule:: drcutils.viz.paper_figures
   :members:
