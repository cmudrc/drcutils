import matplotlib.colors as _mpc


def diverging_hamster_colormap():
    """Diverging colormap with white center"""
    return _mpc.LinearSegmentedColormap(
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


def diverging_hamster_colormap_r():
    """Reversed version of `diverging_hamster_colormap`"""
    cm = diverging_hamster_colormap().reversed()
    cm.name = "diverging_hamster_r"
    return cm


# Diverging colormap, black center
def dark_diverging_hamster_colormap():
    """Diverging colormap with black center"""
    return _mpc.LinearSegmentedColormap(
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


def dark_diverging_hamster_colormap_r():
    """Reversed version of `dark_diverging_hamster_colormap`"""
    cm = dark_diverging_hamster_colormap().reversed()
    cm.name = "dark_diverging_hamster_r"
    return cm


def cool_hamster_colormap():
    """A cool colormap that uses our brand colors"""
    return _mpc.LinearSegmentedColormap(
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


def cool_hamster_colormap_r():
    """Reversed version of `cool_hamster_colormap`"""
    cm = cool_hamster_colormap().reversed()
    cm.name = "cool_hamster_r"
    return cm


def warm_hamster_colormap():
    """A warm colormap that uses our brand colors"""
    return _mpc.LinearSegmentedColormap(
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


def warm_hamster_colormap_r():
    """Reversed version of `warm_hamster_colormap`"""
    cm = warm_hamster_colormap().reversed()
    cm.name = "warm_hamster_r"
    return cm