DOE Utilities
=============

``drcutils.doe.generate_doe`` is a one-stop entrypoint for full factorial,
Latin hypercube, and fractional 2-level workflows.

Quickstart
----------

.. code-block:: python

   from drcutils.doe import generate_doe

   result = generate_doe(
       kind="lhs",
       factors={"temperature": (20.0, 80.0), "pressure": (1.0, 3.0)},
       n_samples=12,
       seed=42,
       randomize=True,
   )

   design = result["design"]
   print(result["summary"])
   print(result["interpretation"])

Optional dependency
-------------------

For larger fractional factorial designs, install optional support:

.. code-block:: bash

   pip install drcutils[doe]

.. automodule:: drcutils.doe.one_stop
   :members:
