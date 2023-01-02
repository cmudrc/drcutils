from __future__ import annotations

import os
import typing

import numpy as _numpy
from plotly.graph_objects import Figure
import plotly.graph_objects as _plotly_graph_objects
import stl as _numpy_stl


def visualize_stl(filepath: str | bytes | os.PathLike,
                  color: typing.Optional[str] = "#ffffff") -> Figure:
    """Visualize an STL.

    Displays the input STL in a Plotly Mesh3d format.

    Parameters
    ----------
    filepath : str | bytes | os.Pathlike
        A filepath to the location of the STL you want to visualize.
    color: str
        The color for the visualization, as a hex code.

    Returns
    -------
    plotly.graph_objects.Figure
        A plotly figure that displays the STl file.

    """
    stl_mesh = _numpy_stl.mesh.Mesh.from_file(filepath)
    # stl_mesh is read by nympy-stl from a stl file; it is  an array of faces/triangles (i.e. three 3d points)
    # this function extracts the unique vertices and the lists I, J, K to define a Plotly mesh3d
    p, q, r = stl_mesh.vectors.shape  # (p, 3, 3)
    # the array stl_mesh.vectors.reshape(p*q, r) can contain multiple copies of the same vertex;
    # extract unique vertices from all mesh triangles
    vertices, ixr = _numpy.unique(stl_mesh.vectors.reshape(p * q, r), return_inverse=True, axis=0)
    I = _numpy.take(ixr, [3 * k for k in range(p)])
    J = _numpy.take(ixr, [3 * k + 1 for k in range(p)])
    K = _numpy.take(ixr, [3 * k + 2 for k in range(p)])
    x, y, z = vertices.T
    colorscale = [[0, color], [1, color]]

    mesh3D = _plotly_graph_objects.Mesh3d(x=x, y=y, z=z, i=I, j=J, k=K, flatshading=True, colorscale=colorscale,
                                          intensity=z, showscale=False)
    layout = _plotly_graph_objects.Layout(
        scene={"xaxis": {"visible": False},
               "yaxis": {"visible": False},
               "zaxis": {"visible": False},
               "aspectmode": "data"
               }
        # scene_xaxis_visible=False,
        # scene_yaxis_visible=False,
        # scene_zaxis_visible=False,
        # scene_aspectmode="data"
    )
    fig = _plotly_graph_objects.Figure(data=[mesh3D], layout=layout)
    fig.data[0].update(
        lighting=dict(ambient=0.18, diffuse=1, fresnel=.1, specular=1, roughness=.1, facenormalsepsilon=0))
    return fig
