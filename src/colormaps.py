import matplotlib.colors


diverging_hamster_colormap = matplotlib.colors.LinearSegmentedColormap(
    "diverging_hamster",
    segmentdata={
        "red": [
            [0.00, 0.10, 0.10],
            [0.17, 0.30, 0.30],
            [0.33, 0.35, 0.35],
            [0.50, 1.00, 1.00],
            [0.75, 0.92, 0.92],
            [1.00, 0.87, 0.87],
        ],
        "green": [
            [0.00, 0.30, 0.30],
            [0.17, 0.53, 0.53],
            [0.33, 0.72, 0.72],
            [0.50, 1.00, 1.00],
            [0.75, 0.52, 0.52],
            [1.00, 0.32, 0.32],
        ],
        "blue": [
            [0.00, 0.29, 0.29],
            [0.17, 0.53, 0.53],
            [0.33, 0.73, 0.73],
            [0.50, 1.00, 1.00],
            [0.75, 0.20, 0.20],
            [1.00, 0.15, 0.15],
        ],
    },
    N=256,
)
diverging_hamster_colormap_r = diverging_hamster_colormap.reversed()
diverging_hamster_colormap_r.name = "diverging_hamster_r"

cool_hamster_colormap = matplotlib.colors.LinearSegmentedColormap(
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
cool_hamster_colormap_r = cool_hamster_colormap.reversed()
cool_hamster_colormap_r.name = "cool_hamster_r"

"""The warm hamster colormap varies from white to black through yellow nd orange colors of the DRC brand"""
warm_hamster_colormap = matplotlib.colors.LinearSegmentedColormap(
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
warm_hamster_colormap_r = warm_hamster_colormap.reversed()
warm_hamster_colormap_r.name = "warm_hamster_r"