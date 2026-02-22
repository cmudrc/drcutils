from __future__ import annotations

import os
import subprocess
import sys


def test_doe_cli_writes_csv(tmp_path) -> None:
    out = tmp_path / "design.csv"
    cmd = [
        sys.executable,
        "-m",
        "drcutils.cli.doe_cli",
        "--kind",
        "lhs",
        "--factors-json",
        '{"x": [0, 1], "y": [10, 20]}',
        "--n-samples",
        "6",
        "--seed",
        "0",
        "--out",
        str(out),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
    assert "Wrote design" in result.stdout
    assert out.exists()
