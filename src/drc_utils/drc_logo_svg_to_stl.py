# -*- coding: utf-8 -*-
"""drc-logo-svg-to-stl.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ef8sdvgFN2s7gY8ZV35TE2wtkhm6NY2P

# Install libraries
"""

import svgpathtools
import numpy
import madcad
import matplotlib.pyplot

paths, attributes = svgpathtools.svg2paths("logo.svg")

N = 25

logo_outline = []
for path in paths[1:]:
    xcoords_for_path = []
    ycoords_for_path = []
    logo_outline_path = []
    for segment in path:
        ts = numpy.linspace(0, 1, int(segment.length()/N) + 2)
        for idx in range(len(ts)-1):
            logo_outline_path.append(
                madcad.primitives.Segment(
                    madcad.vec3(numpy.real(segment.point(ts[idx])), numpy.imag(segment.point(ts[idx])), 0.0),
                    madcad.vec3(numpy.real(segment.point(ts[idx+1])), numpy.imag(segment.point(ts[idx+1])), 0.0)
                )
    logo_outline.append(logo_outline_path)

logo_mesh = madcad.Mesh()
for path in logo_outline:
    logo_mesh += madcad.extrusion(madcad.vec3(0, 0, 1000), madcad.web(path)).orient()
    logo_mesh += madcad.flatsurface(madcad.web(path)).orient(dir = madcad.vec3(0, 0, -1))
    logo_mesh += madcad.flatsurface(madcad.web(path)).transform(madcad.vec3(0, 0, 1000)).orient(dir = madcad.vec3(0, 0, 1))

madcad.write(logo_mesh, "logo.stl")

