import svgpathtools
import PIL
import stl
import pkg_resources


# Path to SVG of logo
SVG_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.svg')

# Path to PNG of logo
PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.png')

# Path to STL of logo
STL_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.stl')

# svgpathtools SVG object of logo
SVG_OBJECT, _ = svgpathtools.svg2paths(SVG_PATH)

# numpy-stl mesh object of logo
MESH_OBJECT = stl.mesh.Mesh.from_file(STL_PATH)

# PIL image object of logo
IMAGE_OBJECT = PIL.Image.open(PNG_PATH)
