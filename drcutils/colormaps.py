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


#: Diverging colormap with white center
diverging_hamster_colormap = _mpc.LinearSegmentedColormap(
    "diverging_hamster",
    segmentdata=_make_segment_data(
        [GREEN, TEAL, TURQUOISE, WHITE, ORANGE, RED],
        [0.00, 0.17, 0.33, 0.50, 0.75, 1.00]
    ),
    N = 256
)
#     {
#         "red": [
#             [0.00, GREEN[0], GREEN[0]],
#             [0.00, TEAL[0], TEAL[0]],
#             [0.00, TURQUOISE[0], TURQUOISE[0]],
#             [0.50, 1.00, 1.00],
#             [0.75, ORANGE[0], ],
#             [1.00, 0.87, 0.87],
#         ],
#         "green": [
#             [0.00, GREEN[1], GREEN[1]],
#             [0.17, 0.53, 0.53],
#             [0.33, 0.72, 0.72],
#             [0.50, 1.00, 1.00],
#             [0.75, 0.52, 0.52],
#             [1.00, 0.32, 0.32],
#         ],
#         "blue": [
#             [0.00, GREEN[2], GREEN[2]],
#             [0.17, 0.53, 0.53],
#             [0.33, 0.73, 0.73],
#             [0.50, 1.00, 1.00],
#             [0.75, 0.20, 0.20],
#             [1.00, 0.15, 0.15],
#         ],
#     },
#     N=256,
# )

#: Reversed version of `diverging_hamster_colormap`
diverging_hamster_colormap_r = diverging_hamster_colormap.reversed()
diverging_hamster_colormap_r.name = "diverging_hamster_r"

#: Diverging colormap, black center
dark_diverging_hamster_colormap = _mpc.LinearSegmentedColormap(
    "dark_diverging_hamster",
    segmentdata={
        "red": [
            [0.00, 0.35, 0.35],
            [0.17, 0.30, 0.30],
            [0.33, 0.10, 0.10],
            [0.50, 0.00, 0.00],
            [0.75, 0.87, 0.87],
            [1.00, 0.92, 0.92],
        ],
        "green": [
            [0.00, 0.72, 0.72],
            [0.17, 0.53, 0.53],
            [0.33, 0.30, 0.30],
            [0.50, 0.00, 0.00],
            [0.75, 0.32, 0.32],
            [1.00, 0.52, 0.52],
        ],
        "blue": [
            [0.00, 0.73, 0.73],
            [0.17, 0.53, 0.53],
            [0.33, 0.29, 0.29],
            [0.50, 0.00, 0.00],
            [0.75, 0.15, 0.15],
            [1.00, 0.20, 0.20],
        ],
    },
    N=256,
)

#: Reversed version of `dark_diverging_hamster_colormap`
dark_diverging_hamster_colormap_r = dark_diverging_hamster_colormap.reversed()
dark_diverging_hamster_colormap_r.name = "dark_diverging_hamster_r"

#: A cool colormap that uses our brand colors
cool_hamster_colormap = _mpc.LinearSegmentedColormap(
    "cool_hamster",
    segmentdata={
        "red": [
            [0.00, 1.00, 1.00],
            [0.25, 0.35, 0.35],
            [0.50, 0.30, 0.30],
            [0.75, 0.10, 0.10],
            [1.00, 0.00, 0.00],
        ],
        "green": [
            [0.00, 1.00, 1.00],
            [0.25, 0.72, 0.72],
            [0.50, 0.53, 0.53],
            [0.75, 0.30, 0.30],
            [1.00, 0.00, 0.00],
        ],
        "blue": [
            [0.00, 1.00, 1.00],
            [0.25, 0.73, 0.73],
            [0.50, 0.53, 0.53],
            [0.75, 0.29, 0.29],
            [1.00, 0.00, 0.00],
        ],
    },
    N=256,
)

#: Reversed version of `cool_hamster_colormap`
cool_hamster_colormap_r = cool_hamster_colormap.reversed()
cool_hamster_colormap_r.name = "cool_hamster_r"

#: A warm colormap that uses our brand colors
warm_hamster_colormap = _mpc.LinearSegmentedColormap(
    "warm_hamster",
    segmentdata={
        "red": [
            [0.00, 1.00, 1.00],
            [0.33, 0.92, 0.92],
            [0.67, 0.87, 0.87],
            [1.00, 0.00, 0.00],
        ],
        "green": [
            [0.00, 1.00, 1.00],
            [0.33, 0.52, 0.52],
            [0.67, 0.32, 0.32],
            [1.00, 0.00, 0.00],
        ],
        "blue": [
            [0.00, 1.00, 1.00],
            [0.33, 0.20, 0.20],
            [0.67, 0.15, 0.15],
            [1.00, 0.00, 0.00],
        ],
    },
    N=256,
)

#: Reversed version of `warm_hamster_colormap`
warm_hamster_colormap_r = warm_hamster_colormap.reversed()
warm_hamster_colormap_r.name = "warm_hamster_r"
