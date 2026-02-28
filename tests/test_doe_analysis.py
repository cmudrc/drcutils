from __future__ import annotations

import importlib.util

import pandas as pd
import pytest

from drcutils.doe import analyze_doe_response, compute_main_effects, fit_screening_model


def _stats_available() -> bool:
    return importlib.util.find_spec("statsmodels") is not None


def test_compute_main_effects_handles_two_level_numeric_factor() -> None:
    df = pd.DataFrame({"x": [0, 0, 1, 1], "yield": [1.0, 2.0, 3.0, 4.0]})

    effects = compute_main_effects(df, response="yield")

    assert list(effects.columns) == [
        "factor",
        "effect_type",
        "effect_estimate",
        "n_levels",
        "low_level",
        "high_level",
    ]
    assert effects.loc[0, "effect_type"] == "two_level_contrast"
    assert effects.loc[0, "effect_estimate"] == pytest.approx(2.0)


def test_compute_main_effects_handles_multilevel_numeric_and_categorical() -> None:
    df = pd.DataFrame(
        {
            "temperature": [10, 20, 30, 10, 20, 30],
            "material": ["a", "b", "c", "a", "b", "c"],
            "yield": [1.0, 2.0, 3.0, 1.5, 2.5, 3.5],
        }
    )

    effects = compute_main_effects(df, response="yield")
    by_factor = effects.set_index("factor")

    assert by_factor.loc["temperature", "effect_type"] == "standardized_slope"
    assert by_factor.loc["material", "effect_type"] == "range_of_group_means"


@pytest.mark.skipif(not _stats_available(), reason="statsmodels is unavailable")
def test_fit_screening_model_returns_expected_columns() -> None:
    df = pd.DataFrame(
        {
            "x1": [0.0, 0.0, 1.0, 1.0, 0.5, 0.5],
            "x2": [0.0, 1.0, 0.0, 1.0, 0.5, 0.2],
            "yield": [1.0, 1.8, 2.0, 2.9, 1.9, 1.6],
        }
    )

    result = fit_screening_model(df, response="yield")

    assert list(result["coefficients"].columns) == [
        "term",
        "coefficient",
        "p_value",
        "ci_low",
        "ci_high",
        "is_significant",
    ]
    assert result["model_summary"]["n_obs"] == 6


def test_fit_screening_model_rejects_nonnumeric_factors() -> None:
    df = pd.DataFrame({"label": ["a", "b", "a", "b"], "yield": [1.0, 2.0, 1.5, 2.5]})

    with pytest.raises(ValueError):
        fit_screening_model(df, response="yield")


def test_analyze_doe_response_skips_model_for_nonnumeric_factors() -> None:
    df = pd.DataFrame({"label": ["a", "b", "a", "b"], "yield": [1.0, 2.0, 1.5, 2.5]})

    result = analyze_doe_response(df, response="yield")

    assert result["model"] is None
    assert result["warnings"]
