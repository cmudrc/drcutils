Bootstrap and Nonparametric Utilities
=====================================

``drcutils.stats`` provides bootstrap confidence intervals, permutation tests,
and automatic rank-test selection with templated interpretation text.

Quickstart
----------

.. code-block:: python

   import numpy as np
   from drcutils.stats import bootstrap_ci, permutation_test, rank_tests_one_stop

   x = np.array([1.2, 1.4, 1.7, 1.6, 1.9])
   y = np.array([1.8, 2.1, 2.0, 2.2, 2.4])

   ci_result = bootstrap_ci(x, stat="mean", seed=0)
   perm_result = permutation_test(x, y, seed=0)
   rank_result = rank_tests_one_stop(x, y=y, paired=False)

   print(ci_result["interpretation"])
   print(perm_result["interpretation"])
   print(rank_result["interpretation"])

Optional dependency
-------------------

Install stats extras for scipy/statsmodels-backed methods:

.. code-block:: bash

   pip install drcutils[stats]

.. automodule:: drcutils.stats.bootstrap_np
   :members:
