import typing

import matplotlib.colors as _matplotlib_colors

from .brand import COLORS as _COLORS

# Unpack colors for easy use
_BLACK, _GREEN, _TEAL, _TURQUOISE, _ORANGE, _RED = [_matplotlib_colors.to_rgb(c) for c in _COLORS]
_WHITE = [1.00, 1.00, 1.00]


def _make_segment_data(colors: typing.Sequence[typing.Any], fractions: typing.Sequence[float]) -> typing.Dict:
    return {
        "red": [[fractions[idx], c[0], c[0]] for idx, c in enumerate(colors)],
        "green": [[fractions[idx], c[1], c[1]] for idx, c in enumerate(colors)],
        "blue": [[fractions[idx], c[2], c[2]] for idx, c in enumerate(colors)]
    }


#: A colormap that simply contains the brand colors
hamster = _matplotlib_colors.ListedColormap(_COLORS, name="hamster")

#: Reversed version of `hamster`
hamster_r = hamster.reversed()

#: Diverging colormap with white center
diverging_hamster = _matplotlib_colors.LinearSegmentedColormap(
    "diverging_hamster",
    segmentdata=_make_segment_data(
        [_GREEN, _TEAL, _TURQUOISE, _WHITE, _ORANGE, _RED],
        [0.00, 0.17, 0.33, 0.50, 0.75, 1.00]
    ),
    N=256
)

#: Reversed version of `diverging_hamster`
diverging_hamster_r = diverging_hamster.reversed()

#: Diverging colormap, black center
dark_diverging_hamster = _matplotlib_colors.LinearSegmentedColormap(
    "dark_diverging_hamster",
    segmentdata=_make_segment_data(
        [_TURQUOISE, _TEAL, _GREEN, _BLACK, _RED, _ORANGE],
        [0.00, 0.17, 0.33, 0.50, 0.75, 1.00]
    ),
    N=256,
)

#: Reversed version of `dark_diverging_hamster`
dark_diverging_hamster_r = dark_diverging_hamster.reversed()

#: A cool colormap that uses our brand colors
cool_hamster = _matplotlib_colors.LinearSegmentedColormap(
    "cool_hamster",
    segmentdata=_make_segment_data(
        [_WHITE, _TURQUOISE, _TEAL, _GREEN, _BLACK],
        [0.00, 0.25, 0.50, 0.75, 1.00]
    ),
    N=256,
)

#: Reversed version of `cool_hamster`
cool_hamster_r = cool_hamster.reversed()

#: A warm colormap that uses our brand colors
warm_hamster = _matplotlib_colors.LinearSegmentedColormap(
    "warm_hamster",
    segmentdata=_make_segment_data(
        [_WHITE, _ORANGE, _RED, _BLACK],
        [0.00, 0.33, 0.67, 1.00]
    ),
    N=256,
)

#: Reversed version of `warm_hamster`
warm_hamster_r = warm_hamster.reversed()
