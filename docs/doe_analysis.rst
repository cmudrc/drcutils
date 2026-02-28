DOE Response Analysis
=====================

Overview
--------

Use ``drcutils.doe`` response-analysis helpers to estimate main effects and
fit lightweight screening models after data collection.

Quick Start
-----------

.. code-block:: python

   import pandas as pd
   from drcutils.doe import analyze_doe_response

   df = pd.read_csv("data/doe_results.csv")
   result = analyze_doe_response(df, response="yield")
   print(result["interpretation"])

CLI
---

.. code-block:: bash

   drc-doe-analyze --input data/doe_results.csv --response-col yield --out-dir artifacts/doe_analysis

Limitations
-----------

- Screening models require numeric factor columns and ``drcutils[stats]``.
- This release focuses on main effects and simple pairwise interactions only.

API Reference
-------------

.. automodule:: drcutils.doe.analysis
   :members:
