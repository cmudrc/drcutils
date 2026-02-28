Dataset Utilities
=================

Overview
--------

Use ``drcutils.dataset`` to profile tabular data, validate CSVs against simple
schemas, and generate lightweight codebooks for lab handoff.

Quick Start
-----------

.. code-block:: python

   import pandas as pd
   from drcutils.dataset import generate_codebook, profile_dataframe, validate_dataframe

   df = pd.read_csv("data/study.csv")
   print(profile_dataframe(df)["warnings"])
   print(validate_dataframe(df, {"participant_id": {"unique": True}})["ok"])
   print(generate_codebook(df).head())

CLI
---

.. code-block:: bash

   drc-data profile --input data/study.csv --out artifacts/profile.json
   drc-data validate --input data/study.csv --schema-file schema.json
   drc-data codebook --input data/study.csv --out artifacts/codebook.csv

Limitations
-----------

- Validation is read-only and never coerces data.
- Schema support is intentionally limited to column-level checks.

API Reference
-------------

.. automodule:: drcutils.dataset
   :members:
