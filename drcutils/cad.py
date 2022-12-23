def visualize_stl(stl, color):
    from plotly.graph_objects import Mesh3d, Layout, Figure
    from numpy import take, unique
    from stl.mesh import Mesh
    stl_mesh = Mesh.from_file(stl)
    # stl_mesh is read by nympy-stl from a stl file; it is  an array of faces/triangles (i.e. three 3d points)
    # this function extracts the unique vertices and the lists I, J, K to define a Plotly mesh3d
    p, q, r = stl_mesh.vectors.shape  # (p, 3, 3)
    # the array stl_mesh.vectors.reshape(p*q, r) can contain multiple copies of the same vertex;
    # extract unique vertices from all mesh triangles
    vertices, ixr = unique(stl_mesh.vectors.reshape(p * q, r), return_inverse=True, axis=0)
    I = take(ixr, [3 * k for k in range(p)])
    J = take(ixr, [3 * k + 1 for k in range(p)])
    K = take(ixr, [3 * k + 2 for k in range(p)])
    x, y, z = vertices.T
    colorscale = [[0, color], [1, color]]

    mesh3D = Mesh3d(x=x, y=y, z=z, i=I, j=J, k=K, flatshading=True, colorscale=colorscale, intensity=z, showscale=False)
    layout = Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False,
        scene_aspectmode="data")
    fig = Figure(data=[mesh3D], layout=layout)
    fig.data[0].update(
        lighting=dict(ambient=0.18, diffuse=1, fresnel=.1, specular=1, roughness=.1, facenormalsepsilon=0))
    return fig
