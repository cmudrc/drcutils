Paper Figure Exporter
=====================

``drcutils.viz.export_figure`` provides a Matplotlib-first export workflow with
preset sizes for one-column papers, two-column papers, and 16:9 slides.

Quickstart
----------

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

.. automodule:: drcutils.viz.paper_figures
   :members:
