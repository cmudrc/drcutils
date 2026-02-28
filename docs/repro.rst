Reproducibility Utilities
=========================

Overview
--------

Use ``drcutils.repro`` to capture portable run-context manifests for figures,
analyses, and ad hoc scripts.

Quick Start
-----------

.. code-block:: python

   from drcutils.repro import capture_run_context, write_run_manifest

   context = capture_run_context(seed=7, input_paths=["data/study.csv"])
   path = write_run_manifest(context, "artifacts/run_context.json")
   print(path)

CLI
---

.. code-block:: bash

   drc-repro snapshot --out artifacts/run_context.json --seed 7 --input data/study.csv

Limitations
-----------

- Git metadata is collected from the current working directory only.
- Input hashing expects file paths, not directories.

API Reference
-------------

.. automodule:: drcutils.repro
   :members:
