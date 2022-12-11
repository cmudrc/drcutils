import matplotlib.pyplot
import matplotlib.colors
import stl
import PIL
import svgpathtools


class logo_only:
    import pkg_resources
    SVG_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.svg')
    PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.png')
    STL_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.stl')
    SVG_OBJECT, _ = svgpathtools.svg2paths(SVG_PATH)
    MESH_OBJECT = stl.mesh.Mesh.from_file(STL_PATH)
    IMAGE_OBJECT = PIL.Image.open(PNG_PATH)
    
    
class horizontal_logo:
    import pkg_resources
    PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/horizontal.png')
    IMAGE_OBJECT = PIL.Image.open(PNG_PATH)

    
class stacked_logo:
    import pkg_resources
    PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/stacked.png')
    IMAGE_OBJECT = PIL.Image.open(PNG_PATH)

    
COLORS = [
    "#000000",
    "#1A4C49",
    "#4C8687",
    "#58B7BB",
    "#EA8534",
    "#DF5227"
]



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


hamster_colormap = matplotlib.colors.LinearSegmentedColormap(
    "hamster",
    segmentdata={
        "red": [
            [0.00, 0.10, 0.10],
            [0.33, 0.30, 0.30],
            [0.67, 0.92, 0.92],
            [1.00, 0.87, 0.87],
        ],
        "green": [
            [0.00, 0.30, 0.30],
            [0.3, 0.53, 0.53],
            [0.67, 0.52, 0.52],
            [1.00, 0.32, 0.32],
        ],
        "blue": [
            [0.00, 0.29, 0.29],
            [0.33, 0.53, 0.53],
            [0.67, 0.20, 0.20],
            [1.00, 0.15, 0.15],
        ],
    },
    N=256,
)
