"""Post-hoc DOE response analysis helpers."""

from __future__ import annotations

from itertools import combinations
from typing import Any

import numpy as np
import pandas as pd
from pandas.api import types as pd_types


def _resolve_factor_columns(
    df: pd.DataFrame,
    *,
    response: str,
    factor_columns: list[str] | None,
) -> list[str]:
    if response not in df.columns:
        raise ValueError(f"Response column '{response}' is missing.")

    resolved = (
        [column for column in df.columns if column != response]
        if factor_columns is None
        else factor_columns
    )
    if not resolved:
        raise ValueError("At least one factor column is required.")

    missing = [column for column in resolved if column not in df.columns]
    if missing:
        raise ValueError(f"Factor columns not found in data: {', '.join(missing)}")
    return resolved


def _sorted_levels(series: pd.Series) -> list[Any]:
    unique_values = series.dropna().unique().tolist()
    if pd_types.is_numeric_dtype(series):
        return sorted(unique_values)
    return sorted(unique_values, key=lambda value: str(value))


def _zscore(values: pd.Series) -> np.ndarray:
    numeric = pd.to_numeric(values, errors="coerce").to_numpy(dtype=float)
    std = float(numeric.std(ddof=0))
    if std == 0:
        return np.zeros_like(numeric, dtype=float)
    return (numeric - float(numeric.mean())) / std


def compute_main_effects(
    df: pd.DataFrame,
    *,
    response: str,
    factor_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Compute main-effect summaries from a DOE response table."""
    resolved_factors = _resolve_factor_columns(df, response=response, factor_columns=factor_columns)
    complete = df.dropna(subset=[response, *resolved_factors]).copy()
    if len(complete) < 4:
        raise ValueError("At least 4 complete rows are required to analyze DOE responses.")

    rows: list[dict[str, Any]] = []
    response_numeric = pd.to_numeric(complete[response], errors="raise")
    response_z = _zscore(response_numeric)

    for factor in resolved_factors:
        series = complete[factor]
        levels = _sorted_levels(series)
        n_levels = len(levels)
        if n_levels == 0:
            continue
        if n_levels == 2:
            low_level, high_level = levels
            low_mean = float(response_numeric.loc[series == low_level].mean())
            high_mean = float(response_numeric.loc[series == high_level].mean())
            rows.append(
                {
                    "factor": factor,
                    "effect_type": "two_level_contrast",
                    "effect_estimate": high_mean - low_mean,
                    "n_levels": n_levels,
                    "low_level": low_level,
                    "high_level": high_level,
                }
            )
            continue

        if pd_types.is_numeric_dtype(series):
            factor_z = _zscore(series)
            effect_estimate = float(np.dot(factor_z, response_z) / max(len(factor_z), 1))
            rows.append(
                {
                    "factor": factor,
                    "effect_type": "standardized_slope",
                    "effect_estimate": effect_estimate,
                    "n_levels": n_levels,
                    "low_level": None,
                    "high_level": None,
                }
            )
        else:
            grouped = complete.groupby(factor, sort=False)[response].mean()
            effect_estimate = float(grouped.max() - grouped.min())
            rows.append(
                {
                    "factor": factor,
                    "effect_type": "range_of_group_means",
                    "effect_estimate": effect_estimate,
                    "n_levels": n_levels,
                    "low_level": None,
                    "high_level": None,
                }
            )

    columns = ["factor", "effect_type", "effect_estimate", "n_levels", "low_level", "high_level"]
    return pd.DataFrame(rows, columns=columns)


def fit_screening_model(
    df: pd.DataFrame,
    *,
    response: str,
    factor_columns: list[str] | None = None,
    include_interactions: bool = False,
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Fit a screening OLS model on numeric DOE factors."""
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1).")

    resolved_factors = _resolve_factor_columns(df, response=response, factor_columns=factor_columns)
    if include_interactions and len(resolved_factors) > 6:
        raise ValueError("Interaction screening supports at most 6 factor columns.")

    nonnumeric = [
        column for column in resolved_factors if not pd_types.is_numeric_dtype(df[column])
    ]
    if nonnumeric:
        raise ValueError("All factor columns must be numeric for screening models.")

    try:
        import statsmodels.api as sm
    except ImportError as exc:
        raise ImportError(
            "DOE screening models require optional stats dependencies. Install with "
            "`pip install drcutils[stats]`."
        ) from exc

    complete = df.dropna(subset=[response, *resolved_factors]).copy()
    response_values = pd.to_numeric(complete[response], errors="raise")
    warnings: list[str] = []

    standardized_terms: dict[str, pd.Series] = {}
    for factor in resolved_factors:
        series = pd.to_numeric(complete[factor], errors="raise")
        std = float(series.std(ddof=0))
        if std == 0:
            warnings.append(f"Factor '{factor}' is constant after filtering complete cases.")
            standardized_terms[factor] = pd.Series(np.zeros(len(series)), index=complete.index)
        else:
            standardized_terms[factor] = (series - float(series.mean())) / std

    design_columns: dict[str, pd.Series] = {}
    for factor in resolved_factors:
        design_columns[factor] = standardized_terms[factor]
    if include_interactions:
        for left, right in combinations(resolved_factors, 2):
            term_name = f"{left}__x__{right}"
            design_columns[term_name] = standardized_terms[left] * standardized_terms[right]

    design = pd.DataFrame(design_columns, index=complete.index)
    design = sm.add_constant(design, has_constant="add")
    design = design.rename(columns={"const": "intercept"})

    n_terms = design.shape[1]
    if len(complete) < (n_terms + 2):
        raise ValueError("At least n_terms + 2 complete rows are required for screening models.")

    matrix = design.to_numpy(dtype=float)
    rank = int(np.linalg.matrix_rank(matrix))
    condition_number = float(np.linalg.cond(matrix))
    if rank < matrix.shape[1]:
        warnings.append("Design matrix is rank-deficient; coefficients may be unstable.")
    if condition_number > 1e8:
        warnings.append("Design matrix is poorly conditioned; coefficients may be unstable.")

    fitted = sm.OLS(response_values.to_numpy(dtype=float), matrix).fit()
    conf_int = fitted.conf_int(alpha=alpha)
    coefficients: list[dict[str, Any]] = []
    column_names = list(design.columns)

    for idx, term in enumerate(column_names):
        p_value = float(fitted.pvalues[idx])
        coefficients.append(
            {
                "term": term,
                "coefficient": float(fitted.params[idx]),
                "p_value": p_value,
                "ci_low": float(conf_int[idx][0]),
                "ci_high": float(conf_int[idx][1]),
                "is_significant": bool(p_value < alpha),
            }
        )

    return {
        "coefficients": pd.DataFrame(
            coefficients,
            columns=["term", "coefficient", "p_value", "ci_low", "ci_high", "is_significant"],
        ),
        "model_summary": {
            "n_obs": int(len(complete)),
            "n_terms": int(n_terms),
            "r_squared": float(fitted.rsquared),
            "adj_r_squared": float(fitted.rsquared_adj),
            "condition_number": condition_number,
        },
        "warnings": warnings,
    }


def analyze_doe_response(
    df: pd.DataFrame,
    *,
    response: str,
    factor_columns: list[str] | None = None,
    include_interactions: bool = False,
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Run a one-stop DOE response analysis."""
    resolved_factors = _resolve_factor_columns(df, response=response, factor_columns=factor_columns)
    complete = df.dropna(subset=[response, *resolved_factors]).copy()
    main_effects = compute_main_effects(
        df,
        response=response,
        factor_columns=resolved_factors,
    )

    warnings: list[str] = []
    model: dict[str, Any] | None = None
    if all(pd_types.is_numeric_dtype(df[column]) for column in resolved_factors):
        model = fit_screening_model(
            df,
            response=response,
            factor_columns=resolved_factors,
            include_interactions=include_interactions,
            alpha=alpha,
        )
        warnings.extend(model["warnings"])
    else:
        warnings.append(
            "Skipped screening model because one or more factor columns are non-numeric."
        )

    interpretation = (
        f"Analyzed {len(resolved_factors)} factor(s); "
        f"{'fit a regression screening model' if model is not None else 'did not fit a regression model'}; "
        f"generated {len(warnings)} warning(s)."
    )

    return {
        "main_effects": main_effects,
        "model": model,
        "summary": {
            "n_rows_analyzed": int(len(complete)),
            "response": response,
            "factor_columns": resolved_factors,
            "include_interactions": bool(include_interactions),
        },
        "warnings": warnings,
        "interpretation": interpretation,
    }
