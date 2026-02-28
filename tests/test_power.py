from __future__ import annotations

import importlib.util

import pytest

import drcutils.power as power_module
from drcutils.power import estimate_sample_size, minimum_detectable_effect, power_curve


def _stats_available() -> bool:
    return importlib.util.find_spec("statsmodels") is not None


@pytest.mark.parametrize("test_name", ["one_sample_t", "paired_t", "two_sample_t"])
@pytest.mark.skipif(not _stats_available(), reason="statsmodels is unavailable")
def test_estimate_sample_size_supported_tests(test_name: str) -> None:
    result = estimate_sample_size(0.5, test=test_name)

    assert result["recommended_n"] > 0
    if test_name == "two_sample_t":
        assert result["group_allocation"] is not None
    else:
        assert result["group_allocation"] is None


def test_estimate_sample_size_rejects_zero_effect() -> None:
    with pytest.raises(ValueError):
        estimate_sample_size(0.0, test="paired_t")


@pytest.mark.skipif(not _stats_available(), reason="statsmodels is unavailable")
def test_power_curve_and_mde_behave_as_expected() -> None:
    curve = power_curve([0.6, 0.2, 0.4], n=48, test="two_sample_t")
    result = minimum_detectable_effect(48, test="two_sample_t", power=0.8)

    assert list(curve.columns) == ["effect_size", "power"]
    assert list(curve["effect_size"]) == [0.6, 0.2, 0.4]
    assert result["minimum_detectable_effect"] > 0
    achieved = power_curve(
        [result["minimum_detectable_effect"]],
        n=48,
        test="two_sample_t",
    ).iloc[0]["power"]
    assert achieved >= 0.79


def test_power_functions_surface_import_error(monkeypatch) -> None:
    def _raise() -> None:
        raise ImportError(
            "Power analysis requires optional stats dependencies. Install with "
            "`pip install drcutils[stats]`."
        )

    monkeypatch.setattr(power_module, "_load_power_engines", _raise)

    with pytest.raises(ImportError, match="Power analysis requires optional stats dependencies"):
        estimate_sample_size(0.5, test="paired_t")
