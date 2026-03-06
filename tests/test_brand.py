from __future__ import annotations

from pathlib import Path

import pytest

from drcutils import brand


def test_palette_matches_official_brand_values() -> None:
    assert brand.BLACK == "#000000"
    assert brand.DARK_TEAL == "#1A4C49"
    assert brand.TEAL == "#4D8687"
    assert brand.BLUE == "#57B7BA"
    assert brand.ORANGE == "#EA8534"
    assert brand.RED == "#DF5127"
    assert brand.COLORS == [
        "#000000",
        "#1A4C49",
        "#4D8687",
        "#57B7BA",
        "#EA8534",
        "#DF5127",
    ]
    assert brand.BRAND_COLORS["dark_teal"] == "#1A4C49"
    assert brand.BRAND_COLORS["red"] == "#DF5127"


def test_flag_default_returns_image() -> None:
    image = brand.flag()
    assert image.mode == "RGB"
    assert image.size == (sum([50, 10, 10, 10, 10, 10]), 100)


def test_flag_custom_segment_widths() -> None:
    widths = [1, 2, 3, 4, 5, 6]
    image = brand.flag(size=[widths, 7])
    assert image.size == (sum(widths), 7)


def test_flag_custom_height_first() -> None:
    widths = [2, 2, 2, 2, 2, 2]
    image = brand.flag(size=[9, widths])
    assert image.size == (12, 9)


@pytest.mark.parametrize(
    "size",
    [
        "bad",
        [1, 2, 3],
        [[1, 2], [3, 4]],
        [[1, 2, 3, 4, 5], 10],
        [[1, 2, 3, 4, 5, 0], 10],
        [[1, 2, 3, 4, 5, 6], 0],
    ],
)
def test_flag_invalid_size_raises(size) -> None:
    with pytest.raises(ValueError):
        brand.flag(size=size)


def test_flag_uses_all_brand_colors() -> None:
    image = brand.flag(size=[[1] * len(brand.COLORS), 1])
    # One pixel per brand color.
    assert image.size[0] == len(brand.COLORS)


@pytest.mark.parametrize(
    ("layout", "variants"),
    [
        ("horizontal", ["full", "black", "dark_teal", "red", "white"]),
        ("stacked", ["full", "black", "dark_teal", "red", "white"]),
        ("symbol", ["full", "black", "dark_teal", "blue", "teal", "orange", "red", "white"]),
    ],
)
def test_logo_path_matrix_resolves(layout: str, variants: list[str]) -> None:
    for variant in variants:
        assert Path(brand.get_logo_path(layout, variant)).exists()
    assert Path(brand.get_logo_path(layout, "auto")).exists()
    assert Path(brand.get_logo_path(layout, "full", on_black=True)).exists()


def test_logo_path_validation_errors() -> None:
    with pytest.raises(ValueError, match="layout"):
        brand.get_logo_path("unsupported", "full")
    with pytest.raises(ValueError, match="variant"):
        brand.get_logo_path("horizontal", "blue")
    with pytest.raises(ValueError, match="PNG"):
        brand.get_logo_path("horizontal", "full", fmt="svg")


def test_pattern_gradient_circle_and_scribble_paths_resolve() -> None:
    for variant in ["full", "grey", "white", "gray"]:
        assert Path(brand.get_pattern_path(variant)).exists()

    gradients = brand.get_gradient_paths()
    assert len(gradients) == 6
    assert [Path(path).name for path in gradients] == ["01.png", "02.png", "03.png", "04.png", "05.png", "06.png"]
    assert all(Path(path).exists() for path in gradients)

    for color in ["blue", "dark_teal", "orange", "red", "teal", "white"]:
        assert Path(brand.get_circle_graphic_path(color)).exists()
        assert Path(brand.get_scribble_path("thin", color)).exists()
        assert Path(brand.get_scribble_path("thick", color)).exists()


def test_matplotlib_font_fallbacks_exposed() -> None:
    fallbacks = brand.get_matplotlib_font_fallbacks()
    assert fallbacks["primary"][0] == "Magdelin"
    assert fallbacks["secondary"][0] == "Zilla Slab"
    assert brand.PRIMARY_FONT_USAGE == "ALL CAPS headers"
    assert brand.SECONDARY_FONT_USAGE == "body text"
