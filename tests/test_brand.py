from __future__ import annotations

import pytest

from drcutils.brand import COLORS, flag


def test_flag_default_returns_image() -> None:
    image = flag()
    assert image.mode == "RGB"
    assert image.size == (sum([50, 10, 10, 10, 10, 10]), 100)


def test_flag_custom_segment_widths() -> None:
    widths = [1, 2, 3, 4, 5, 6]
    image = flag(size=[widths, 7])
    assert image.size == (sum(widths), 7)


def test_flag_custom_height_first() -> None:
    widths = [2, 2, 2, 2, 2, 2]
    image = flag(size=[9, widths])
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
        flag(size=size)


def test_flag_uses_all_brand_colors() -> None:
    image = flag(size=[[1] * len(COLORS), 1])
    # One pixel per brand color.
    assert image.size[0] == len(COLORS)
