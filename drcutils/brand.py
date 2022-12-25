import pkg_resources

#: The colors of the DRC brand
COLORS = [
    "#000000",
    "#1A4C49",
    "#4C8687",
    "#58B7BB",
    "#EA8534",
    "#DF5227"
]

#: Path to an SVG of logo
LOGO_ONLY_SVG = pkg_resources.resource_filename('drcutils', 'data/logo.svg')

#: Path to a PNG of logo
LOGO_ONLY_PNG = pkg_resources.resource_filename('drcutils', 'data/logo.png')

#: Path to an STL of logo
LOGO_ONLY_STL = pkg_resources.resource_filename('drcutils', 'data/logo.stl')

#: Path to a PNG of the horizontal logo
HORIZONTAL_LOGO_PNG = pkg_resources.resource_filename('drcutils', 'data/horizontal.png')

#: Path to a PNG of the stacked logo
STACKED_LOGO_PNG = pkg_resources.resource_filename('drcutils', 'data/stacked.png')
