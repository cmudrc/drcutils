"""Power and sample-size planning helpers."""

from __future__ import annotations

import math
from typing import Any

import pandas as pd

_POWER_IMPORT_ERROR = (
    "Power analysis requires optional stats dependencies. Install with "
    "`pip install drcutils[stats]`."
)
_SUPPORTED_TESTS = {"one_sample_t", "paired_t", "two_sample_t"}
_SUPPORTED_ALTERNATIVES = {"two-sided", "larger", "smaller"}


def _load_power_engines() -> tuple[Any, Any]:
    try:
        from statsmodels.stats.power import TTestIndPower, TTestPower
    except ImportError as exc:
        raise ImportError(_POWER_IMPORT_ERROR) from exc
    return TTestIndPower(), TTestPower()


def _validate_common_inputs(
    *,
    test: str,
    alpha: float,
    power: float | None = None,
    ratio: float = 1.0,
    alternative: str,
) -> None:
    if test not in _SUPPORTED_TESTS:
        valid = ", ".join(sorted(_SUPPORTED_TESTS))
        raise ValueError(f"test must be one of: {valid}")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1).")
    if power is not None and not (0.0 < power < 1.0):
        raise ValueError("power must be in (0, 1).")
    if ratio <= 0:
        raise ValueError("ratio must be positive.")
    if alternative not in _SUPPORTED_ALTERNATIVES:
        valid = ", ".join(sorted(_SUPPORTED_ALTERNATIVES))
        raise ValueError(f"alternative must be one of: {valid}")


def _two_sample_allocation_from_n(total_n: int, ratio: float) -> tuple[int, int]:
    n1 = max(1, int(round(total_n / (1.0 + ratio))))
    if n1 >= total_n:
        n1 = total_n - 1
    n2 = total_n - n1
    if n2 <= 0:
        n2 = 1
        n1 = total_n - n2
    return n1, n2


def _compute_power(
    effect_size: float,
    *,
    n: int,
    test: str,
    alpha: float,
    ratio: float,
    alternative: str,
) -> float:
    ind_power, one_power = _load_power_engines()
    effect = abs(effect_size)
    if test == "two_sample_t":
        n1, n2 = _two_sample_allocation_from_n(n, ratio)
        return float(
            ind_power.power(
                effect_size=effect,
                nobs1=n1,
                alpha=alpha,
                ratio=(n2 / n1),
                alternative=alternative,
            )
        )
    return float(one_power.power(effect_size=effect, nobs=n, alpha=alpha, alternative=alternative))


def estimate_sample_size(
    effect_size: float,
    *,
    test: str,
    alpha: float = 0.05,
    power: float = 0.8,
    ratio: float = 1.0,
    alternative: str = "two-sided",
) -> dict[str, Any]:
    """Estimate total sample size for supported t-test families."""
    _validate_common_inputs(
        test=test,
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative=alternative,
    )

    effect = abs(effect_size)
    if effect == 0:
        raise ValueError("effect_size must be non-zero.")

    ind_power, one_power = _load_power_engines()
    assumptions = ["Effect size is interpreted as Cohen's d."]

    if test == "two_sample_t":
        nobs1 = float(
            ind_power.solve_power(
                effect_size=effect,
                nobs1=None,
                alpha=alpha,
                power=power,
                ratio=ratio,
                alternative=alternative,
            )
        )
        n1 = max(1, int(math.ceil(nobs1)))
        n2 = max(1, int(math.ceil(n1 * ratio)))
        recommended_n = n1 + n2
        group_allocation: list[int] | None = [n1, n2]
        assumptions.append("Group allocation is rounded up while preserving the requested ratio.")
    else:
        nobs = float(
            one_power.solve_power(
                effect_size=effect,
                nobs=None,
                alpha=alpha,
                power=power,
                alternative=alternative,
            )
        )
        recommended_n = max(2, int(math.ceil(nobs)))
        group_allocation = None

    return {
        "test": test,
        "effect_size": effect,
        "alpha": alpha,
        "target_power": power,
        "alternative": alternative,
        "recommended_n": int(recommended_n),
        "group_allocation": group_allocation,
        "assumptions": assumptions,
    }


def power_curve(
    effect_sizes: list[float],
    *,
    n: int,
    test: str,
    alpha: float = 0.05,
    ratio: float = 1.0,
    alternative: str = "two-sided",
) -> pd.DataFrame:
    """Compute achieved power over a sequence of effect sizes."""
    _validate_common_inputs(
        test=test,
        alpha=alpha,
        ratio=ratio,
        alternative=alternative,
    )
    if not effect_sizes:
        raise ValueError("effect_sizes must not be empty.")
    if n <= 1:
        raise ValueError("n must be greater than 1.")

    rows = [
        {
            "effect_size": abs(effect_size),
            "power": _compute_power(
                abs(effect_size),
                n=n,
                test=test,
                alpha=alpha,
                ratio=ratio,
                alternative=alternative,
            ),
        }
        for effect_size in effect_sizes
    ]
    return pd.DataFrame(rows, columns=["effect_size", "power"])


def minimum_detectable_effect(
    n: int,
    *,
    test: str,
    alpha: float = 0.05,
    power: float = 0.8,
    ratio: float = 1.0,
    alternative: str = "two-sided",
) -> dict[str, Any]:
    """Solve for the smallest detectable standardized effect size."""
    _validate_common_inputs(
        test=test,
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative=alternative,
    )
    if n <= 1:
        raise ValueError("n must be greater than 1.")

    low = 1e-6
    high = 5.0
    if (
        _compute_power(high, n=n, test=test, alpha=alpha, ratio=ratio, alternative=alternative)
        < power
    ):
        raise ValueError("Target power is unreachable for effect sizes up to 5.0.")

    for _ in range(100):
        mid = (low + high) / 2.0
        achieved = _compute_power(
            mid,
            n=n,
            test=test,
            alpha=alpha,
            ratio=ratio,
            alternative=alternative,
        )
        if achieved >= power:
            high = mid
        else:
            low = mid
        if abs(high - low) < 1e-4:
            break

    return {
        "test": test,
        "n": int(n),
        "alpha": alpha,
        "target_power": power,
        "alternative": alternative,
        "minimum_detectable_effect": float(high),
        "assumptions": ["Effect size is interpreted as Cohen's d."],
    }
