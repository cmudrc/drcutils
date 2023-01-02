from __future__ import annotations

import os
import typing

import numpy as _numpy
import plotly.graph_objects as _plotly_graph_objects
import stl as _numpy_stl
from plotly.graph_objects import Figure


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
    x_indices = _numpy.take(ixr, [3 * k for k in range(p)])
    y_indices = _numpy.take(ixr, [3 * k + 1 for k in range(p)])
    z_indices = _numpy.take(ixr, [3 * k + 2 for k in range(p)])
    x, y, z = vertices.T
    colorscale = [[0, color], [1, color]]

    mesh = _plotly_graph_objects.Mesh3d(x=x, y=y, z=z, i=x_indices, j=y_indices, k=z_indices, flatshading=True,
                                        colorscale=colorscale, intensity=z, showscale=False)

    # Set layout to hide things we don't care about
    layout = _plotly_graph_objects.Layout(
        scene={
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "zaxis": {"visible": False},
            "aspectmode": "data"
        }
    )

    # Plot the thing
    fig = _plotly_graph_objects.Figure(data=[mesh], layout=layout)

    # Set lighting
    fig.data[0].update(
        lighting=dict(ambient=0.18, diffuse=1, fresnel=.1, specular=1, roughness=.1, facenormalsepsilon=0))

    return fig
