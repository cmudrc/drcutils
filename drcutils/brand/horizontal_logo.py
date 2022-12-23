import pkg_resources
import PIL

# Path to PNG of horizontal logo
PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/horizontal.png')

# PIL image object of horizontal logo
IMAGE_OBJECT = PIL.Image.open(PNG_PATH)
