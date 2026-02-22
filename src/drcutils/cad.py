"""CAD helpers for STL visualization."""

from __future__ import annotations

from os import PathLike

import numpy as _np
from stl.mesh import Mesh as _Mesh


def visualize_stl(filepath: str | bytes | PathLike, color: str = "#ffffff"):
    """Visualize an STL mesh as a Plotly figure.

    Args:
        filepath: Path to the STL file.
        color: Hex color used for mesh shading.

    Returns:
        A Plotly figure containing a single ``Mesh3d`` trace.

    Raises:
        ImportError: If Plotly is not installed.
    """
    try:
        from plotly.graph_objects import Figure as _Figure
        from plotly.graph_objects import Layout as _Layout
        from plotly.graph_objects import Mesh3d as _Mesh3d
    except ImportError as exc:
        raise ImportError(
            "Plotly is optional for CAD visualization. Install with `pip install drcutils[plotly]`."
        ) from exc

    stl_mesh = _Mesh.from_file(filepath)
    p, q, r = stl_mesh.vectors.shape
    vertices, ixr = _np.unique(stl_mesh.vectors.reshape(p * q, r), return_inverse=True, axis=0)
    i_idx = _np.take(ixr, [3 * k for k in range(p)])
    j_idx = _np.take(ixr, [3 * k + 1 for k in range(p)])
    k_idx = _np.take(ixr, [3 * k + 2 for k in range(p)])
    x_vals, y_vals, z_vals = vertices.T
    colorscale = [[0, color], [1, color]]

    mesh_3d = _Mesh3d(
        x=x_vals,
        y=y_vals,
        z=z_vals,
        i=i_idx,
        j=j_idx,
        k=k_idx,
        flatshading=True,
        colorscale=colorscale,
        intensity=z_vals,
        showscale=False,
    )
    layout = _Layout(
        scene_xaxis_visible=False,
        scene_yaxis_visible=False,
        scene_zaxis_visible=False,
        scene_aspectmode="data",
    )
    fig = _Figure(data=[mesh_3d], layout=layout)
    fig.data[0].update(
        lighting={
            "ambient": 0.18,
            "diffuse": 1.0,
            "fresnel": 0.1,
            "specular": 1.0,
            "roughness": 0.1,
            "facenormalsepsilon": 0,
        }
    )
    return fig
