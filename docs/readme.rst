Getting Started
===============

Install
-------

.. code-block:: bash

   pip install drcutils

Optional Extras
---------------

.. code-block:: bash

   pip install drcutils[doe]
   pip install drcutils[stats]
   pip install drcutils[plotly]

Choose Your Import Style
------------------------

Use the flat API for quick scripts:

.. code-block:: python

   from drcutils import bootstrap_ci, export_figure, generate_doe

Or import by domain when you want a clearer namespace:

.. code-block:: python

   from drcutils.stats import bootstrap_ci
   from drcutils.viz import export_figure
   from drcutils.doe import generate_doe

The same domain-first pattern applies to ``drcutils.brand``,
``drcutils.data``, and ``drcutils.runtime``.

Quick Examples
--------------

.. code-block:: python

   import pandas as pd

   from drcutils import bootstrap_ci
   from drcutils.doe import generate_doe
   from drcutils.viz import export_figure

   ci = bootstrap_ci([1, 2, 3, 4, 5], stat="mean", seed=0)

   design = generate_doe(
       kind="lhs",
       factors={"temperature": (20.0, 80.0), "pressure": (1.0, 3.0)},
       n_samples=12,
       seed=42,
   )

   df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 4]})
   fig = df.plot(x="x", y="y").get_figure()
   export_figure(fig, "artifacts/figures/main_result")

   print(ci["interpretation"])
   print(design["summary"]["n_runs"])
