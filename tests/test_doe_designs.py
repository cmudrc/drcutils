from __future__ import annotations

import numpy as np

from drcutils.doe.designs import full_factorial, latin_hypercube


def test_full_factorial_row_count() -> None:
    design = full_factorial({"a": [0, 1], "b": [10, 20, 30]})
    assert len(design) == 6


def test_lhs_deterministic_seed() -> None:
    factors = {"x": (0.0, 1.0), "y": (10.0, 20.0)}
    d1 = latin_hypercube(8, factors=factors, seed=4)
    d2 = latin_hypercube(8, factors=factors, seed=4)
    assert np.allclose(d1.to_numpy(), d2.to_numpy())
