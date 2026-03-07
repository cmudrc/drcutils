"""Matplotlib colormaps derived from DRC brand colors."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

import matplotlib.colors as _mpc

from . import BLACK, BLUE, COLORS, DARK_TEAL, ORANGE, RED, TEAL

_BLACK_RGB, _DARK_TEAL_RGB, _TEAL_RGB, _BLUE_RGB, _ORANGE_RGB, _RED_RGB = [
    _mpc.to_rgb(c) for c in COLORS
]
_WHITE_RGB = (1.0, 1.0, 1.0)

type _ChannelStops = Sequence[tuple[float, ...]]
type _SegmentData = dict[Literal["red", "green", "blue", "alpha"], _ChannelStops]


def _make_segment_data(
    colors: Sequence[Sequence[float]],
    fractions: Sequence[float],
) -> _SegmentData:
    return {
        "red": [(fractions[idx], c[0], c[0]) for idx, c in enumerate(colors)],
        "green": [(fractions[idx], c[1], c[1]) for idx, c in enumerate(colors)],
        "blue": [(fractions[idx], c[2], c[2]) for idx, c in enumerate(colors)],
        "alpha": [(fractions[idx], 1.0, 1.0) for idx, _ in enumerate(colors)],
    }


#: Listed colormap in canonical DRC palette order.
drc_palette = _mpc.ListedColormap(COLORS, name="drc_palette")
drc_palette_r = drc_palette.reversed()
drc_palette_r.name = "drc_palette_r"

#: Diverging colormap with white center.
drc_diverging = _mpc.LinearSegmentedColormap(
    "drc_diverging",
    segmentdata=_make_segment_data(
        [_DARK_TEAL_RGB, _TEAL_RGB, _BLUE_RGB, _WHITE_RGB, _ORANGE_RGB, _RED_RGB],
        [0.00, 0.17, 0.33, 0.50, 0.75, 1.00],
    ),
    N=256,
)
drc_diverging_r = drc_diverging.reversed()
drc_diverging_r.name = "drc_diverging_r"

#: Diverging colormap with a dark center.
drc_dark_diverging = _mpc.LinearSegmentedColormap(
    "drc_dark_diverging",
    segmentdata=_make_segment_data(
        [_BLUE_RGB, _TEAL_RGB, _DARK_TEAL_RGB, _BLACK_RGB, _RED_RGB, _ORANGE_RGB],
        [0.00, 0.17, 0.33, 0.50, 0.75, 1.00],
    ),
    N=256,
)
drc_dark_diverging_r = drc_dark_diverging.reversed()
drc_dark_diverging_r.name = "drc_dark_diverging_r"

#: Cool gradient from white to black through blue/teal tones.
drc_cool = _mpc.LinearSegmentedColormap(
    "drc_cool",
    segmentdata=_make_segment_data(
        [_WHITE_RGB, _BLUE_RGB, _TEAL_RGB, _DARK_TEAL_RGB, _BLACK_RGB],
        [0.00, 0.25, 0.50, 0.75, 1.00],
    ),
    N=256,
)
drc_cool_r = drc_cool.reversed()
drc_cool_r.name = "drc_cool_r"

#: Warm gradient from white to black through orange/red tones.
drc_warm = _mpc.LinearSegmentedColormap(
    "drc_warm",
    segmentdata=_make_segment_data(
        [_WHITE_RGB, _ORANGE_RGB, _RED_RGB, _BLACK_RGB], [0.00, 0.33, 0.67, 1.00]
    ),
    N=256,
)
drc_warm_r = drc_warm.reversed()
drc_warm_r.name = "drc_warm_r"

__all__ = [
    "BLACK",
    "BLUE",
    "DARK_TEAL",
    "ORANGE",
    "RED",
    "TEAL",
    "drc_cool",
    "drc_cool_r",
    "drc_dark_diverging",
    "drc_dark_diverging_r",
    "drc_diverging",
    "drc_diverging_r",
    "drc_palette",
    "drc_palette_r",
    "drc_warm",
    "drc_warm_r",
]
