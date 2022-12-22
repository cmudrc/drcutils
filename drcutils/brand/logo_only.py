import svgpathtools
import PIL
import stl
import pkg_resources

SVG_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.svg')
PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.png')
STL_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.stl')
SVG_OBJECT, _ = svgpathtools.svg2paths(SVG_PATH)
MESH_OBJECT = stl.mesh.Mesh.from_file(STL_PATH)
IMAGE_OBJECT = PIL.Image.open(PNG_PATH)