from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from drcutils.visualization import export_figure
from drcutils.visualization.plotting import (
    get_plot_palette,
    get_plot_rcparams,
    get_plot_style_path,
    get_plotly_template,
    plot_style_context,
    use_plot_style,
)


def test_get_plot_style_path_resolves_packaged_file() -> None:
    assert get_plot_style_path().endswith("drc.mplstyle")
    assert Path(get_plot_style_path()).is_file()


def test_get_plot_palette_uses_expected_display_order() -> None:
    assert get_plot_palette() == [
        "#1A4C49",
        "#57B7BA",
        "#EA8534",
        "#DF5127",
        "#4D8687",
        "#000000",
    ]


@pytest.mark.parametrize(
    ("context", "expected"),
    [
        ("paper", {"font.size": 9.0, "axes.titlesize": 10.0, "savefig.dpi": 300}),
        ("notebook", {"font.size": 11.0, "axes.titlesize": 12.0, "savefig.dpi": 150}),
        ("talk", {"font.size": 14.0, "axes.titlesize": 16.0, "savefig.dpi": 200}),
    ],
)
def test_get_plot_rcparams_context_values(context: str, expected: dict[str, float]) -> None:
    rcparams = get_plot_rcparams(context=context)  # type: ignore[arg-type]
    for key, value in expected.items():
        assert rcparams[key] == value


def test_get_plot_rcparams_rejects_unknown_context() -> None:
    with pytest.raises(ValueError, match="Unknown plotting context"):
        get_plot_rcparams("poster")  # type: ignore[arg-type]


def test_use_plot_style_updates_matplotlib_rcparams() -> None:
    with mpl.rc_context():
        use_plot_style(context="paper")
        assert mpl.rcParams["image.cmap"] == "drc_diverging"
        assert mpl.rcParams["font.serif"][0] == "Zilla Slab"
        assert list(mpl.rcParams["axes.prop_cycle"].by_key()["color"]) == get_plot_palette()
        assert mpl.rcParams["lines.linewidth"] == 2.0


def test_plot_style_context_restores_rcparams() -> None:
    original_size = mpl.rcParams["font.size"]
    with plot_style_context(context="talk"):
        assert mpl.rcParams["font.size"] == 14.0
    assert mpl.rcParams["font.size"] == original_size


def test_use_plot_style_missing_seaborn_dependency(monkeypatch) -> None:
    def _fake_import(name: str) -> object:
        if name == "seaborn":
            raise ImportError("missing seaborn")
        raise AssertionError(f"Unexpected module request: {name}")

    monkeypatch.setattr("drcutils.viz.plotting._import_module", _fake_import)

    with mpl.rc_context(), pytest.raises(ImportError, match="drcutils\\[visualization\\]"):
        use_plot_style(context="paper", seaborn=True)


def test_use_plot_style_calls_seaborn_with_expected_palette(monkeypatch) -> None:
    recorded: dict[str, object] = {}

    def _set_theme(**kwargs: object) -> None:
        recorded.update(kwargs)

    fake_seaborn = SimpleNamespace(set_theme=_set_theme)
    monkeypatch.setattr("drcutils.viz.plotting._import_module", lambda _: fake_seaborn)

    with mpl.rc_context():
        use_plot_style(context="notebook", seaborn=True)

    assert recorded["style"] == "whitegrid"
    assert recorded["context"] == "notebook"
    assert recorded["palette"] == get_plot_palette()
    assert recorded["rc"]["font.size"] == 11.0


def test_pandas_plot_inherits_theme() -> None:
    with plot_style_context(context="paper"):
        ax = pd.DataFrame({"value": [1, 2, 3]}).plot()
        line_color = mcolors.to_hex(ax.get_lines()[0].get_color())
        assert line_color.lower() == get_plot_palette()[0].lower()
        plt.close(ax.figure)


def test_get_plotly_template_has_expected_shape() -> None:
    template = get_plotly_template()
    assert template["layout"]["colorway"] == get_plot_palette()
    assert template["layout"]["font"]["color"] == "#000000"
    assert len(template["layout"]["colorscale"]["sequential"]) == 11
    assert len(template["layout"]["colorscale"]["sequentialminus"]) == 11
    assert len(template["layout"]["colorscale"]["diverging"]) == 11


def test_get_plotly_template_wraps_in_plotly_when_available() -> None:
    go = pytest.importorskip("plotly.graph_objects")
    template = go.layout.Template(get_plotly_template())
    assert list(template.layout.colorway) == get_plot_palette()


def test_visualization_namespace_matches_viz_exports() -> None:
    from drcutils import visualization, viz

    assert visualization.use_plot_style is viz.use_plot_style
    assert visualization.export_figure is viz.export_figure


def test_export_figure_with_plot_style_context(tmp_path) -> None:
    with plot_style_context(context="paper"):
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 4], label="trend")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()

        result = export_figure(fig, tmp_path / "styled_figure", formats=["png"])

        assert len(result["files"]) == 1
        assert result["files"][0].exists()

        plt.close(fig)
