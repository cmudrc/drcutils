from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pandas as pd


def _run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    return subprocess.run(
        [sys.executable, *args],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def _invalid_child_path(tmp_path: Path, child_name: str) -> str:
    blocker = tmp_path / "not_a_directory"
    blocker.write_text("block parent directory creation", encoding="utf-8")
    return str(blocker / child_name)


def test_doe_cli_output_path_error_returns_error_code(tmp_path) -> None:
    bad_output_path = _invalid_child_path(tmp_path, "out.csv")
    result = _run_cli(
        [
            "-m",
            "drcutils.cli.doe_cli",
            "--kind",
            "lhs",
            "--factors-json",
            '{"x": [0, 1], "y": [10, 20]}',
            "--n-samples",
            "4",
            "--out",
            bad_output_path,
        ]
    )

    assert result.returncode == 2
    assert "Failed to create output directory" in result.stderr


def test_doe_analysis_cli_output_path_error_returns_error_code(tmp_path) -> None:
    csv_path = tmp_path / "doe.csv"
    pd.DataFrame(
        {
            "factor": ["a", "b", "a", "b"],
            "yield": [1.0, 2.0, 1.5, 2.5],
        }
    ).to_csv(csv_path, index=False)

    bad_output_path = _invalid_child_path(tmp_path, "out")
    result = _run_cli(
        [
            "-m",
            "drcutils.cli.doe_analysis_cli",
            "--input",
            str(csv_path),
            "--response-col",
            "yield",
            "--out-dir",
            bad_output_path,
        ]
    )

    assert result.returncode == 2
    assert "Failed to create output directory" in result.stderr
