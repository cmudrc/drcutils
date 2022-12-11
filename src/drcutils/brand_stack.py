class logo_only:
    from stl import mesh
    import PIL
    import pkg_resources
    SVG_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.svg')
    STL_PATH = pkg_resources.resource_filename('drcutils', 'data/logo.stl')
    MESH_OBJECT = stl.mesh.Mesh.form_file(STL_PATH)
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
    "#1A4C9",
    "#4C8687",
    "#58B7BB",
    "#EA8534",
    "#DF5227"
]
