from __future__ import annotations

import numpy as np

from drcutils.stats import rank_tests_one_stop


def test_rank_test_selection_unpaired() -> None:
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2, 3, 4, 5, 6], dtype=float)
    result = rank_tests_one_stop(x, y=y, paired=False)
    assert result["test"] == "mannwhitney"


def test_rank_test_selection_paired() -> None:
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([1.2, 2.1, 3.1, 4.1, 5.1], dtype=float)
    result = rank_tests_one_stop(x, y=y, paired=True)
    assert result["test"] == "wilcoxon"


def test_rank_tests_requires_scipy_for_runtime() -> None:
    # If scipy is missing in runtime env, function should raise ImportError with extra hint.
    # This test is permissive: if scipy exists, behavior should still be valid.
    x = np.array([1, 2, 3], dtype=float)
    y = np.array([1, 2, 4], dtype=float)
    try:
        result = rank_tests_one_stop(x, y=y, paired=False)
    except ImportError as exc:
        assert "drcutils[stats]" in str(exc)
    else:
        assert "test" in result
