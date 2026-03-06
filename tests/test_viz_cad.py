from __future__ import annotations

import builtins
import sys
from types import ModuleType, SimpleNamespace

import numpy as np
import pytest

import drcutils.viz.cad as cad


class _FakeMesh3d:
    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs
        self.updated: dict[str, object] = {}

    def update(self, **kwargs: object) -> None:
        self.updated.update(kwargs)


class _FakeLayout:
    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs


class _FakeFigure:
    def __init__(self, data: list[_FakeMesh3d], layout: _FakeLayout) -> None:
        self.data = data
        self.layout = layout


class _FakeStlMesh:
    def __init__(self) -> None:
        self.vectors = np.array(
            [
                [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            ],
            dtype=float,
        )


def test_visualize_stl_success_with_mocked_plotly(monkeypatch) -> None:
    fake_go = ModuleType("plotly.graph_objects")
    fake_go.Figure = _FakeFigure
    fake_go.Layout = _FakeLayout
    fake_go.Mesh3d = _FakeMesh3d

    fake_plotly = ModuleType("plotly")
    fake_plotly.graph_objects = fake_go

    monkeypatch.setitem(sys.modules, "plotly", fake_plotly)
    monkeypatch.setitem(sys.modules, "plotly.graph_objects", fake_go)
    monkeypatch.setattr(cad, "_Mesh", SimpleNamespace(from_file=lambda _: _FakeStlMesh()))

    fig = cad.visualize_stl("dummy.stl", color="#123456")

    assert isinstance(fig, _FakeFigure)
    mesh = fig.data[0]
    assert mesh.kwargs["colorscale"] == [[0, "#123456"], [1, "#123456"]]
    assert mesh.kwargs["flatshading"] is True
    assert "lighting" in mesh.updated


def test_visualize_stl_missing_plotly_dependency(monkeypatch) -> None:
    original_import = builtins.__import__

    def _mock_import(name: str, *args: object, **kwargs: object) -> object:
        if name == "plotly.graph_objects":
            raise ImportError("missing plotly")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _mock_import)

    with pytest.raises(ImportError, match="pip install drcutils\\[plotly\\]"):
        cad.visualize_stl("dummy.stl")
