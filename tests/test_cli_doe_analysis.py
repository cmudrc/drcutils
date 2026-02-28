from __future__ import annotations

import json
import os
import subprocess
import sys

import pandas as pd


def test_doe_analysis_cli_writes_outputs(tmp_path) -> None:
    csv_path = tmp_path / "doe.csv"
    out_dir = tmp_path / "analysis"
    pd.DataFrame(
        {
            "label": ["a", "b", "a", "b"],
            "yield": [1.0, 2.0, 1.5, 2.5],
        }
    ).to_csv(csv_path, index=False)

    cmd = [
        sys.executable,
        "-m",
        "drcutils.cli.doe_analysis_cli",
        "--input",
        str(csv_path),
        "--response-col",
        "yield",
        "--out-dir",
        str(out_dir),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)

    assert (out_dir / "main_effects.csv").exists()
    assert (out_dir / "summary.json").exists()
    assert (
        json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))["summary"]["response"]
        == "yield"
    )
    assert "Analyzed 1 factor(s)" in result.stdout
