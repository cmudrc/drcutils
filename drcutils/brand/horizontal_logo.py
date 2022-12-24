import pkg_resources
import PIL

#: Path to PNG of the horizontal logo
PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/horizontal.png')

#: PIL image object of the horizontal logo
IMAGE_OBJECT = PIL.Image.open(PNG_PATH)
