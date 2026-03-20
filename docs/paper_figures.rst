Paper Figure Exporter
=====================

Overview
--------

Use ``drcutils.visualization.export_figure`` to export Matplotlib figures with
publication-friendly presets and consistent output naming.

Quick Start
-----------

.. code-block:: python

   import matplotlib.pyplot as plt
   from drcutils.visualization import export_figure, use_plot_style

   use_plot_style(context="paper")
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

Style Note
----------

``export_figure()`` preserves the figure you pass in. Apply
``use_plot_style(context="paper")`` before creating the figure when you want
the shared DRC theme in addition to the export presets.

API Reference
-------------

.. automodule:: drcutils.visualization.paper_figures
   :members:
