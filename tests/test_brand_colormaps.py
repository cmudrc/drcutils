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
    assert colormaps.hamster.name == "hamster"
    assert colormaps.hamster_r.name == "hamster_r"

    assert colormaps.diverging_hamster.name == "diverging_hamster"
    assert colormaps.diverging_hamster_r.name == "diverging_hamster_r"

    assert colormaps.dark_diverging_hamster.name == "dark_diverging_hamster"
    assert colormaps.dark_diverging_hamster_r.name == "dark_diverging_hamster_r"

    assert colormaps.cool_hamster.name == "cool_hamster"
    assert colormaps.cool_hamster_r.name == "cool_hamster_r"

    assert colormaps.warm_hamster.name == "warm_hamster"
    assert colormaps.warm_hamster_r.name == "warm_hamster_r"


def test_colormap_sampling_returns_rgba() -> None:
    rgba = colormaps.diverging_hamster(0.5)
    assert len(rgba) == 4
    assert all(0.0 <= value <= 1.0 for value in rgba)
