import pkg_resources
import PIL

PNG_PATH = pkg_resources.resource_filename('drcutils', 'data/horizontal.png')
IMAGE_OBJECT = PIL.Image.open(PNG_PATH)
