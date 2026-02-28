from __future__ import annotations

import json
import os
import subprocess
import sys


def test_repro_cli_snapshot_writes_json(tmp_path) -> None:
    input_path = tmp_path / "input.csv"
    input_path.write_text("value\n1\n", encoding="utf-8")
    out_path = tmp_path / "context.json"

    cmd = [
        sys.executable,
        "-m",
        "drcutils.cli.repro_cli",
        "snapshot",
        "--out",
        str(out_path),
        "--input",
        str(input_path),
        "--seed",
        "9",
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)

    assert out_path.exists()
    assert str(out_path.resolve()) in result.stdout
    assert json.loads(out_path.read_text(encoding="utf-8"))["random_seed"] == 9
