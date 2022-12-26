from __future__ import annotations

from plotly.graph_objects import Mesh3d as _Mesh3d, Layout as _Layout, Figure as _Figure
from numpy import take as _take, unique as _unique
from stl.mesh import Mesh as _Mesh
from os import PathLike


def visualize_stl(filepath: str | bytes | PathLike, color: str = "#ffffff") -> _Figure:
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
    Plotly.graph_objects.Figure
        A plotly figure that displays the STl file.

    """
    stl_mesh = _Mesh.from_file(filepath)
    # stl_mesh is read by nympy-stl from a stl file; it is  an array of faces/triangles (i.e. three 3d points)
    # this function extracts the unique vertices and the lists I, J, K to define a Plotly mesh3d
    p, q, r = stl_mesh.vectors.shape  # (p, 3, 3)
    # the array stl_mesh.vectors.reshape(p*q, r) can contain multiple copies of the same vertex;
    # extract unique vertices from all mesh triangles
    vertices, ixr = _unique(stl_mesh.vectors.reshape(p * q, r), return_inverse=True, axis=0)
    I = _take(ixr, [3 * k for k in range(p)])
    J = _take(ixr, [3 * k + 1 for k in range(p)])
    K = _take(ixr, [3 * k + 2 for k in range(p)])
    x, y, z = vertices.T
    colorscale = [[0, color], [1, color]]

    mesh3D = _Mesh3d(x=x, y=y, z=z, i=I, j=J, k=K, flatshading=True, colorscale=colorscale, intensity=z, showscale=False)
    layout = _Layout(
        scene_xaxis_visible=False,
        scene_yaxis_visible=False,
        scene_zaxis_visible=False,
        scene_aspectmode="data"
    )
    fig = _Figure(data=[mesh3D], layout=layout)
    fig.data[0].update(
        lighting=dict(ambient=0.18, diffuse=1, fresnel=.1, specular=1, roughness=.1, facenormalsepsilon=0))
    return fig
