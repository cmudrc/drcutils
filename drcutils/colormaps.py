import typing

import matplotlib.colors as _matplotlib_colors
from matplotlib.colors import LinearSegmentedColormap

from .brand import COLORS as _COLORS

# Unpack colors for easy use
_BLACK, _GREEN, _TEAL, _TURQUOISE, _ORANGE, _RED = [_matplotlib_colors.to_rgb(c) for c in _COLORS]
_WHITE = [1.00, 1.00, 1.00]

# Define the ColorLike type
ColorLike = typing.TypeVar('ColorLike', str, typing.Sequence[float], typing.Tuple[float, float, float],
                           typing.Tuple[float, float, float, float])


def make_colormap(name: str, colors: typing.Sequence[ColorLike], fractions: typing.Sequence[float],
                  N: int = 256) -> LinearSegmentedColormap:
    """Make a colormap based on a sequence of colors and intervals.

    Specifically, this function makes a LinearSegmentedColormap for use with matplotlib.

    Parameters
    ----------
    name : str
        The name of the colormap
    colors: Sequence[ColorLike]
        The series of colors to use.
    fractions: Sequence[float
        The fractional interval at which each color should be placed.
    N: int
        Number of fractions to make the colormap with

    Returns
    -------
    LinearSegmentedColormap
        Returns a matplotlib.colors.LinearSegmentedColormap object.

    """
    # Verify colors
    for color in colors:
        if not _matplotlib_colors.is_color_like(color):
            raise ValueError(f"The color {color} is not recognized as a valid matplotlib color.")

    # Convert colors to rgb
    colors = [_matplotlib_colors.to_rgb(c) for c in colors]

    # Make a dict of data
    segment_data = {
        "red": [[fractions[idx], c[0], c[0]] for idx, c in enumerate(colors)],
        "green": [[fractions[idx], c[1], c[1]] for idx, c in enumerate(colors)],
        "blue": [[fractions[idx], c[2], c[2]] for idx, c in enumerate(colors)]
    }

    # Return a colormap
    return _matplotlib_colors.LinearSegmentedColormap(
        name,
        segmentdata=segment_data,
        N=N,
    )


#: A colormap that simply contains the brand colors
hamster = _matplotlib_colors.ListedColormap(_COLORS, name="hamster")

#: Reversed version of `hamster`
hamster_r = hamster.reversed()

#: Diverging colormap with white center
diverging_hamster = make_colormap(
    "diverging_hamster",
    [_GREEN, _TEAL, _TURQUOISE, _WHITE, _ORANGE, _RED],
    [0.00, 0.17, 0.33, 0.50, 0.75, 1.00],
    N=256
)

#: Reversed version of `diverging_hamster`
diverging_hamster_r = diverging_hamster.reversed()

#: Diverging colormap, black center
dark_diverging_hamster = make_colormap(
    "dark_diverging_hamster",
    [_TURQUOISE, _TEAL, _GREEN, _BLACK, _RED, _ORANGE],
    [0.00, 0.17, 0.33, 0.50, 0.75, 1.00],
    N=256,
)

#: Reversed version of `dark_diverging_hamster`
dark_diverging_hamster_r = dark_diverging_hamster.reversed()

#: A cool colormap that uses our brand colors
cool_hamster = make_colormap(
    "cool_hamster",
    [_WHITE, _TURQUOISE, _TEAL, _GREEN, _BLACK],
    [0.00, 0.25, 0.50, 0.75, 1.00],
    N=256,
)

#: Reversed version of `cool_hamster`
cool_hamster_r = cool_hamster.reversed()

#: A warm colormap that uses our brand colors
warm_hamster = make_colormap(
    "warm_hamster",
    [_WHITE, _ORANGE, _RED, _BLACK],
    [0.00, 0.33, 0.67, 1.00],
    N=256,
)

#: Reversed version of `warm_hamster`
warm_hamster_r = warm_hamster.reversed()
