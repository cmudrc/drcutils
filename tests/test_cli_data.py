from __future__ import annotations

import json
import os
import subprocess
import sys

import pandas as pd


def test_data_cli_profile_writes_json(tmp_path) -> None:
    csv_path = tmp_path / "data.csv"
    pd.DataFrame({"value": [1, 2, 3]}).to_csv(csv_path, index=False)
    out_path = tmp_path / "profile.json"

    cmd = [
        sys.executable,
        "-m",
        "drcutils.cli.data_cli",
        "profile",
        "--input",
        str(csv_path),
        "--out",
        str(out_path),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)

    assert json.loads(out_path.read_text(encoding="utf-8"))["n_rows"] == 3


def test_data_cli_validate_returns_error_exit_code(tmp_path) -> None:
    csv_path = tmp_path / "data.csv"
    pd.DataFrame({"value": [1, 2, 3]}).to_csv(csv_path, index=False)

    cmd = [
        sys.executable,
        "-m",
        "drcutils.cli.data_cli",
        "validate",
        "--input",
        str(csv_path),
        "--schema-json",
        '{"missing": {"required": true}}',
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(cmd, env=env, check=False, capture_output=True, text=True)

    assert result.returncode == 2


def test_data_cli_validate_returns_warning_exit_code_when_requested(tmp_path) -> None:
    csv_path = tmp_path / "data.csv"
    schema_path = tmp_path / "schema.json"
    pd.DataFrame({"value": [1, 2, 3], "extra": [4, 5, 6]}).to_csv(csv_path, index=False)
    schema_path.write_text(json.dumps({"value": {"required": True}}), encoding="utf-8")

    cmd = [
        sys.executable,
        "-m",
        "drcutils.cli.data_cli",
        "validate",
        "--input",
        str(csv_path),
        "--schema-file",
        str(schema_path),
        "--fail-on-warning",
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(cmd, env=env, check=False, capture_output=True, text=True)

    assert result.returncode == 3


def test_data_cli_codebook_writes_csv(tmp_path) -> None:
    csv_path = tmp_path / "data.csv"
    out_path = tmp_path / "codebook.csv"
    pd.DataFrame({"value": [1, 2, 3]}).to_csv(csv_path, index=False)

    cmd = [
        sys.executable,
        "-m",
        "drcutils.cli.data_cli",
        "codebook",
        "--input",
        str(csv_path),
        "--out",
        str(out_path),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)

    assert out_path.exists()
    assert "Wrote codebook" in result.stdout
