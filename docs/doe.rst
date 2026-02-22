DOE Utilities
=============

Overview
--------

Use ``drcutils.doe.generate_doe`` to create and summarize full factorial,
Latin hypercube, and fractional 2-level designs.

Quick Start
-----------

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

Optional Extras
---------------

For larger fractional factorial workflows, install optional DOE support:

.. code-block:: bash

   pip install drcutils[doe]

API Reference
-------------

.. automodule:: drcutils.doe.one_stop
   :members:
