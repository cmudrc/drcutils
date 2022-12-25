import matplotlib.colors as _mpc
from .brand import COLORS

BLACK, GREEN, TEAL, TURQUOISE, ORANGE, RED = [_mpc.to_rgb(c) for c in COLORS]
WHITE = [1.00, 1.00, 1.00]


def _make_segment_data(colors, fractions):
    return {
        "red": [[fractions[idx], c[0], c[0]] for idx, c in enumerate(colors)],
        "green": [[fractions[idx], c[1], c[1]] for idx, c in enumerate(colors)],
        "blue": [[fractions[idx], c[2], c[2]] for idx, c in enumerate(colors)]
    }


#: A colormap that simply contains the brand colors
hamster = _mpc.ListedColormap(COLORS, name="hamster")

#: Reversed version of `hamster`
hamster_r = hamster.reversed()
hamster_r.name = "hamster_r"

#: Diverging colormap with white center
diverging_hamster = _mpc.LinearSegmentedColormap(
    "diverging_hamster",
    segmentdata=_make_segment_data(
        [GREEN, TEAL, TURQUOISE, WHITE, ORANGE, RED],
        [0.00, 0.17, 0.33, 0.50, 0.75, 1.00]
    ),
    N=256
)

#: Reversed version of `diverging_hamster`
diverging_hamster_r = diverging_hamster.reversed()
diverging_hamster_r.name = "diverging_hamster_r"

#: Diverging colormap, black center
dark_diverging_hamster = _mpc.LinearSegmentedColormap(
    "dark_diverging_hamster",
    segmentdata=_make_segment_data(
        [TURQUOISE, TEAL, GREEN, BLACK, RED, ORANGE],
        [0.00, 0.17, 0.33, 0.50, 0.75, 1.00]
    ),
    N=256,
)

#: Reversed version of `dark_diverging_hamster`
dark_diverging_hamster_r = dark_diverging_hamster.reversed()
dark_diverging_hamster_r.name = "dark_diverging_hamster_r"

#: A cool colormap that uses our brand colors
cool_hamster = _mpc.LinearSegmentedColormap(
    "cool_hamster",
    segmentdata=_make_segment_data(
        [WHITE, TURQUOISE, TEAL, GREEN, BLACK],
        [0.00, 0.25, 0.50, 0.75, 1.00]
    ),
    N=256,
)

#: Reversed version of `cool_hamster`
cool_hamster_r = cool_hamster.reversed()
cool_hamster_r.name = "cool_hamster_r"

#: A warm colormap that uses our brand colors
warm_hamster = _mpc.LinearSegmentedColormap(
    "warm_hamster",
    segmentdata=_make_segment_data(
        [WHITE, ORANGE, RED, BLACK],
        [0.00, 0.33, 0.67, 1.00]
    ),
    N=256,
)

#: Reversed version of `warm_hamster`
warm_hamster_r = warm_hamster.reversed()
warm_hamster_r.name = "warm_hamster_r"
