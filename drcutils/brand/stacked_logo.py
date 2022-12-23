import pkg_resources
import PIL

# Path to PNG of stacked logo
PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/stacked.png')

# PIL image object of stacked logo
IMAGE_OBJECT = PIL.Image.open(PNG_PATH)
