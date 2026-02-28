from __future__ import annotations

from unittest.mock import patch

import drcutils.viz.ml as ml


def test_visualize_network_colab_branch() -> None:
    with (
        patch("drcutils.viz.ml._serve") as serve,
        patch("drcutils.viz.ml._display") as display,
        patch("drcutils.viz.ml.is_notebook", return_value=True),
        patch("drcutils.viz.ml.is_google_colab", return_value=True),
    ):
        ml.visualize_network("model.onnx", height=400, port=8001)

    serve.assert_called_once_with("model.onnx", None, ("localhost", 8001), False, 0)
    js = display.call_args[0][0].data
    assert "proxyPort(8001)" in js


def test_visualize_network_notebook_non_colab_branch() -> None:
    with (
        patch("drcutils.viz.ml._serve") as serve,
        patch("drcutils.viz.ml._display") as display,
        patch("drcutils.viz.ml.is_notebook", return_value=True),
        patch("drcutils.viz.ml.is_google_colab", return_value=False),
    ):
        ml.visualize_network("model.onnx", height=500, port=8123)

    serve.assert_called_once_with("model.onnx", None, ("localhost", 8123), False, 0)
    js = display.call_args[0][0].data
    assert "http://localhost:8123" in js


def test_visualize_network_terminal_branch() -> None:
    with (
        patch("drcutils.viz.ml._serve") as serve,
        patch("drcutils.viz.ml._display") as display,
        patch("drcutils.viz.ml.is_notebook", return_value=False),
    ):
        ml.visualize_network("model.onnx", port=9000)

    serve.assert_called_once_with("model.onnx", None, ("localhost", 9000), True, 0)
    display.assert_not_called()
