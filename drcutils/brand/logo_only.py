import svgpathtools
import PIL
import stl
import pkg_resources


#: Path to SVG of logo
SVG_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.svg')

#: Path to PNG of logo
PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.png')

#: Path to STL of logo
STL_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.stl')

#: An svgpathtools object of the logo
SVG_OBJECT, _ = svgpathtools.svg2paths(SVG_PATH)

#: A numpy-stl mesh object of the logo
MESH_OBJECT = stl.mesh.Mesh.from_file(STL_PATH)

#: PIL image object of the logo
IMAGE_OBJECT = PIL.Image.open(PNG_PATH)
