from __future__ import annotations

import importlib.util
import os
import subprocess
import sys

import pytest


def _stats_available() -> bool:
    return importlib.util.find_spec("statsmodels") is not None


@pytest.mark.skipif(not _stats_available(), reason="statsmodels is unavailable")
def test_power_cli_curve_writes_csv(tmp_path) -> None:
    out_path = tmp_path / "curve.csv"
    cmd = [
        sys.executable,
        "-m",
        "drcutils.cli.power_cli",
        "curve",
        "--test",
        "two_sample_t",
        "--n",
        "48",
        "--effect-sizes-json",
        "[0.2, 0.4, 0.6]",
        "--out",
        str(out_path),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)

    assert out_path.exists()
    assert "Wrote power curve" in result.stdout
