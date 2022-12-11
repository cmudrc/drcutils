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
    IMAGE_OBJECT = PIL.Image.open(SVG_PATH)
    
    
# class horizontal_logo:
#     import pkg_resources
#     SVG = pkg_resources.resource_filename('drcutils', 'data/logo.svg')
#     STL = pkg_resources.resource_filename('drcutils', 'data/logo.stl')

# class stacked_logo:
#     import pkg_resources
#     SVG = pkg_resources.resource_filename('drcutils', 'data/logo.svg')
#     STL = pkg_resources.resource_filename('drcutils', 'data/logo.stl')

COLORS = [
    "#000000",
    "#1A4C49",
    "#4C8687",
    "#58B7BB",
    "#EA8534",
    "#DF5227"
]
