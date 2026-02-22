"""Design of experiments (DOE) primitive generators."""

from __future__ import annotations

from itertools import product
from typing import Any

import numpy as np
import pandas as pd


def full_factorial(levels: dict[str, list[Any] | np.ndarray]) -> pd.DataFrame:
    """Generate a full-factorial design.

    Args:
        levels: Mapping from factor name to explicit levels.

    Returns:
        A DataFrame with all combinations of provided levels.
    """
    factors = list(levels.keys())
    level_lists = [list(levels[name]) for name in factors]
    rows = list(product(*level_lists))
    return pd.DataFrame(rows, columns=factors)


def latin_hypercube(
    n_samples: int,
    factors: dict[str, tuple[float, float]],
    seed: int = 0,
) -> pd.DataFrame:
    """Generate a deterministic Latin hypercube sample for bounded factors.

    Args:
        n_samples: Number of design points.
        factors: Mapping from factor name to numeric bounds ``(low, high)``.
        seed: Random seed.

    Returns:
        A DataFrame with one sampled value per stratum for each factor.
    """
    if n_samples <= 0:
        raise ValueError("n_samples must be positive.")

    rng = np.random.default_rng(seed)
    data: dict[str, np.ndarray] = {}
    for name, (low, high) in factors.items():
        if not high > low:
            raise ValueError(f"Factor '{name}' bounds must satisfy high > low.")
        cut_points = np.linspace(0.0, 1.0, n_samples + 1)
        points = cut_points[:-1] + rng.random(n_samples) * (cut_points[1:] - cut_points[:-1])
        rng.shuffle(points)
        data[name] = low + points * (high - low)

    return pd.DataFrame(data)


def randomize_runs(df: pd.DataFrame, seed: int = 0, block: str | None = None) -> pd.DataFrame:
    """Randomize run order globally or within blocks.

    Args:
        df: Design DataFrame.
        seed: Random seed.
        block: Optional blocking column for within-block randomization.

    Returns:
        A randomized DataFrame with a reset index.
    """
    if block is not None:
        if block not in df.columns:
            raise ValueError(f"Block column '{block}' not present in design.")
        groups = []
        for _, group in df.groupby(block, sort=False):
            groups.append(group.sample(frac=1, random_state=seed))
        return pd.concat(groups, ignore_index=True)
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


_FRACFACT_DESIGNS_RES3: dict[int, str] = {
    4: "a b c abc",
    5: "a b c abc ac",
    6: "a b c abc ac bc",
}


def fractional_factorial_2level(factors: list[str], resolution: str = "III") -> pd.DataFrame:
    """Generate a two-level fractional-factorial design.

    Args:
        factors: Factor names.
        resolution: Desired resolution string. Currently supports ``III``.

    Returns:
        A DataFrame with coded levels in ``{-1, +1}``.

    Raises:
        ImportError: If optional ``pyDOE2`` support is required.
    """
    if resolution != "III":
        raise ValueError("Only resolution 'III' is currently supported.")
    if len(factors) < 2:
        raise ValueError("At least two factors are required for a factorial design.")

    if len(factors) <= 3:
        coded = np.array(list(product([-1.0, 1.0], repeat=len(factors))))
        return pd.DataFrame(coded, columns=factors)

    try:
        from pyDOE2 import fracfact
    except ImportError as exc:
        raise ImportError(
            "Fractional factorial designs for >3 factors require pyDOE2. "
            "Install with `pip install drcutils[doe]`."
        ) from exc

    if len(factors) not in _FRACFACT_DESIGNS_RES3:
        raise ImportError(
            "Fallback templates support only up to 6 factors. "
            "Install with `pip install drcutils[doe]` and provide a custom design if needed."
        )

    coded = fracfact(_FRACFACT_DESIGNS_RES3[len(factors)])
    return pd.DataFrame(coded, columns=factors)


def design_balance_report(design: pd.DataFrame) -> dict[str, dict[str, float]]:
    """Compute a simple per-factor balance report.

    Args:
        design: Design DataFrame.

    Returns:
        Mapping of factor to unique level counts and imbalance ratios.
    """
    report: dict[str, dict[str, float]] = {}
    for column in design.columns:
        counts = design[column].value_counts(dropna=False).astype(float)
        ratio = float(counts.max() / counts.min()) if len(counts) > 1 else 1.0
        report[column] = {
            "n_levels": float(len(counts)),
            "max_to_min_ratio": ratio,
        }
    return report
