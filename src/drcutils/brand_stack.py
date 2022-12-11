import stl
import PIL
import svgpathtools
import matplotlib.colors

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
