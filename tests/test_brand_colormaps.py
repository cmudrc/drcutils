from __future__ import annotations

import drcutils.brand as brand
import drcutils.brand.colormaps as colormaps


def test_lazy_colormaps_access_via_brand_getattr() -> None:
    assert brand.colormaps is colormaps


def test_make_segment_data_shape() -> None:
    data = colormaps._make_segment_data(
        colors=[(0.0, 0.5, 1.0), (1.0, 0.0, 0.5)],
        fractions=[0.0, 1.0],
    )

    assert sorted(data.keys()) == ["blue", "green", "red"]
    assert data["red"][0] == [0.0, 0.0, 0.0]
    assert data["blue"][1] == [1.0, 0.5, 0.5]


def test_named_colormaps_and_reversed_names() -> None:
    assert colormaps.drc_palette.name == "drc_palette"
    assert colormaps.drc_palette_r.name == "drc_palette_r"

    assert colormaps.drc_diverging.name == "drc_diverging"
    assert colormaps.drc_diverging_r.name == "drc_diverging_r"

    assert colormaps.drc_dark_diverging.name == "drc_dark_diverging"
    assert colormaps.drc_dark_diverging_r.name == "drc_dark_diverging_r"

    assert colormaps.drc_cool.name == "drc_cool"
    assert colormaps.drc_cool_r.name == "drc_cool_r"

    assert colormaps.drc_warm.name == "drc_warm"
    assert colormaps.drc_warm_r.name == "drc_warm_r"


def test_colormap_sampling_returns_rgba() -> None:
    rgba = colormaps.drc_diverging(0.5)
    assert len(rgba) == 4
    assert all(0.0 <= value <= 1.0 for value in rgba)


def test_legacy_hamster_names_are_removed() -> None:
    assert not hasattr(colormaps, "hamster")
    assert not hasattr(colormaps, "cool_hamster")
    assert not hasattr(colormaps, "warm_hamster")
