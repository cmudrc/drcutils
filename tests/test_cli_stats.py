from __future__ import annotations

import os
import subprocess
import sys

import pandas as pd


def test_stats_cli_bootstrap(tmp_path) -> None:
    path = tmp_path / "data.csv"
    pd.DataFrame({"value": [1, 2, 3, 4, 5]}).to_csv(path, index=False)

    cmd = [
        sys.executable,
        "-m",
        "drcutils.cli.stats_cli",
        "bootstrap-ci",
        "--input",
        str(path),
        "--column",
        "value",
        "--stat",
        "mean",
        "--seed",
        "1",
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
    assert "estimate" in result.stdout
