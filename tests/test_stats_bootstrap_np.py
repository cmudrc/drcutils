from __future__ import annotations

import numpy as np

from drcutils.stats import bootstrap_ci, permutation_test


def test_bootstrap_ci_deterministic_bounds() -> None:
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    result = bootstrap_ci(x, stat="mean", n_resamples=4000, seed=2)
    assert 1.5 < result["ci_low"] < 3.2
    assert 3.0 < result["ci_high"] < 4.8


def test_permutation_detects_shift() -> None:
    rng = np.random.default_rng(7)
    x = rng.normal(0.0, 1.0, 80)
    y = rng.normal(1.0, 1.0, 80)
    result = permutation_test(x, y, n_permutations=5000, seed=7)
    assert result["p_value"] < 0.05
