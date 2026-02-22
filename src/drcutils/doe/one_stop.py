"""High-level one-stop DOE generation workflows."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .designs import (
    design_balance_report,
    fractional_factorial_2level,
    full_factorial,
    latin_hypercube,
    randomize_runs,
)


def generate_doe(
    *,
    kind: str,
    factors: dict[str, Any],
    n_samples: int | None = None,
    seed: int = 0,
    center_points: int = 0,
    replicates: int = 1,
    randomize: bool = True,
) -> dict[str, Any]:
    """Generate and summarize a DOE table.

    Args:
        kind: Design kind: ``full``, ``lhs``, or ``frac2``.
        factors: Factor specification map.
        n_samples: Number of samples for LHS.
        seed: Random seed.
        center_points: Number of center points to append.
        replicates: Number of full design replicates.
        randomize: Whether to randomize run order.

    Returns:
        Structured dictionary with design, summary, interpretation, and warnings.
    """
    warnings: list[str] = []
    if replicates <= 0:
        raise ValueError("replicates must be positive.")

    if kind == "full":
        design = full_factorial(factors)
    elif kind == "lhs":
        if n_samples is None:
            raise ValueError("n_samples is required for lhs designs.")
        design = latin_hypercube(n_samples=n_samples, factors=factors, seed=seed)
    elif kind == "frac2":
        design = fractional_factorial_2level(factors=list(factors.keys()))
    else:
        raise ValueError("kind must be one of: full, lhs, frac2")

    if replicates > 1:
        design = pd.concat([design.copy() for _ in range(replicates)], ignore_index=True)

    if center_points > 0:
        center_row = {}
        for name in design.columns:
            col = design[name]
            if np.issubdtype(col.dtype, np.number):
                center_row[name] = float(col.min() + col.max()) / 2.0
            else:
                center_row[name] = col.mode(dropna=False).iloc[0]
        cp_df = pd.DataFrame([center_row] * center_points)
        design = pd.concat([design, cp_df], ignore_index=True)

    if randomize:
        design = randomize_runs(design, seed=seed)

    ranges = {
        name: [float(design[name].min()), float(design[name].max())]
        for name in design.columns
        if np.issubdtype(design[name].dtype, np.number)
    }
    balance = design_balance_report(design)
    for name, stats in balance.items():
        if stats["max_to_min_ratio"] > 2.0:
            warnings.append(f"Factor '{name}' appears imbalanced (max/min ratio > 2).")

    summary = {
        "n_runs": int(len(design)),
        "factors": list(design.columns),
        "ranges": ranges,
        "design_kind": kind,
        "balance": balance,
    }

    interpretation = (
        f"Generated a {kind} DOE with {len(design)} runs across {len(design.columns)} factors. "
        "The summary includes numeric ranges and a balance report for quick diagnostics. "
        "Use randomization seeds for reproducible execution order."
    )

    return {
        "design": design,
        "summary": summary,
        "interpretation": interpretation,
        "warnings": warnings,
    }
