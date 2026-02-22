from __future__ import annotations

import matplotlib.pyplot as plt

from drcutils.viz import export_figure, get_figure_preset


def test_get_figure_preset_known_target() -> None:
    preset = get_figure_preset("one_col")
    assert preset["width"] > 0
    assert preset["height"] > 0


def test_export_figure_multi_target_multi_format(tmp_path) -> None:
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 4], label="curve")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()

    result = export_figure(
        fig,
        tmp_path / "figure",
        targets=["one_col", "slide_16x9"],
        formats=["pdf", "png"],
        dpi=120,
    )

    assert len(result["files"]) == 4
    for out in result["files"]:
        assert out.exists()
        assert out.stat().st_size > 0

    plt.close(fig)
