Power Utilities
===============

Overview
--------

Use ``drcutils.power`` for quick power and sample-size planning around t-test
study designs.

Quick Start
-----------

.. code-block:: python

   from drcutils.power import estimate_sample_size, minimum_detectable_effect, power_curve

   print(estimate_sample_size(0.5, test="two_sample_t"))
   print(minimum_detectable_effect(48, test="paired_t"))
   print(power_curve([0.2, 0.4, 0.6], n=48, test="two_sample_t"))

CLI
---

.. code-block:: bash

   drc-power sample-size --test two_sample_t --effect-size 0.5
   drc-power curve --test paired_t --n 48 --effect-sizes-json "[0.2, 0.4, 0.6]" --out artifacts/power_curve.csv

Limitations
-----------

- Only one-sample, paired, and two-sample t-test families are supported.
- These helpers require ``drcutils[stats]``.

API Reference
-------------

.. automodule:: drcutils.power
   :members:
