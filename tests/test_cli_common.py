from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from drcutils.cli import _common as common


def test_build_parser_sets_prog_and_description() -> None:
    parser = common.build_parser(prog="demo-cli", description="Demo parser.")
    assert parser.prog == "demo-cli"
    assert parser.description == "Demo parser."


def test_parse_json_helpers_success_and_shape_validation() -> None:
    assert common.parse_json_argument('{"a": 1}', label="--payload") == {"a": 1}
    assert common.parse_json_object('{"a": 1}', label="--payload") == {"a": 1}
    assert common.parse_json_list("[1, 2, 3]", label="--items") == [1, 2, 3]

    with pytest.raises(ValueError, match="must decode to a JSON object"):
        common.parse_json_object("[1, 2, 3]", label="--payload")
    with pytest.raises(ValueError, match="must decode to a JSON list"):
        common.parse_json_list('{"a": 1}', label="--items")


def test_parse_json_argument_invalid_json_raises() -> None:
    with pytest.raises(ValueError, match="Invalid --payload"):
        common.parse_json_argument("{bad json", label="--payload")


def test_read_json_file_paths(tmp_path: Path) -> None:
    good = tmp_path / "good.json"
    good.write_text('{"ok": true}', encoding="utf-8")
    assert common.read_json_file(good, label="config") == {"ok": True}

    missing = tmp_path / "missing.json"
    with pytest.raises(ValueError, match="config not found"):
        common.read_json_file(missing, label="config")

    bad = tmp_path / "bad.json"
    bad.write_text("{bad", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid config"):
        common.read_json_file(bad, label="config")

    directory = tmp_path / "as_dir"
    directory.mkdir()
    with pytest.raises(ValueError, match="Failed to read config"):
        common.read_json_file(directory, label="config")


def test_ensure_parent_dir_and_directory_error_paths(tmp_path: Path) -> None:
    blocker = tmp_path / "not_a_dir"
    blocker.write_text("x", encoding="utf-8")

    with pytest.raises(ValueError, match="Failed to create output directory"):
        common.ensure_parent_dir(blocker / "child.json")

    with pytest.raises(ValueError, match="Failed to create output directory"):
        common.ensure_directory(blocker / "child")


def test_write_json_file_and_write_csv_file_success(tmp_path: Path) -> None:
    out_json = tmp_path / "nested" / "data.json"
    payload = {"b": 2, "a": 1}
    common.write_json_file(out_json, payload)
    assert out_json.exists()
    assert out_json.read_text(encoding="utf-8").endswith("\n")

    out_csv = tmp_path / "nested" / "data.csv"
    frame = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    common.write_csv_file(out_csv, frame)
    restored = pd.read_csv(out_csv)
    assert list(restored.columns) == ["x", "y"]


def test_write_json_file_open_error_is_wrapped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out_json = tmp_path / "out.json"

    def _raise_oserror(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise OSError("disk full")

    monkeypatch.setattr(Path, "open", _raise_oserror)
    with pytest.raises(ValueError, match="Failed to write JSON"):
        common.write_json_file(out_json, {"a": 1})


def test_write_csv_file_to_csv_error_is_wrapped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out_csv = tmp_path / "out.csv"
    frame = pd.DataFrame({"x": [1]})

    def _raise_oserror(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise OSError("write blocked")

    monkeypatch.setattr(pd.DataFrame, "to_csv", _raise_oserror)
    with pytest.raises(ValueError, match="Failed to write CSV"):
        common.write_csv_file(out_csv, frame)


def test_read_csv_success_and_error_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    good = tmp_path / "good.csv"
    pd.DataFrame({"x": [1, 2]}).to_csv(good, index=False)
    result = common.read_csv(good)
    assert list(result["x"]) == [1, 2]

    with pytest.raises(ValueError, match="Input CSV not found"):
        common.read_csv(tmp_path / "missing.csv")

    def _raise_parse_error(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise pd.errors.ParserError("bad csv")

    monkeypatch.setattr(pd, "read_csv", _raise_parse_error)
    with pytest.raises(ValueError, match="Failed to parse CSV"):
        common.read_csv(good)

    def _raise_oserror(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise OSError("io failure")

    monkeypatch.setattr(pd, "read_csv", _raise_oserror)
    with pytest.raises(ValueError, match="Failed to read CSV"):
        common.read_csv(good)


def test_parse_comma_list_behaviors() -> None:
    assert common.parse_comma_list(None) is None
    assert common.parse_comma_list("a,b, c") == ["a", "b", "c"]
    assert common.parse_comma_list(" , , ") is None


def test_print_helpers(capsys: pytest.CaptureFixture[str]) -> None:
    common.print_json({"b": 2, "a": 1})
    assert '"a": 1' in capsys.readouterr().out

    code = common.print_error("failed")
    captured = capsys.readouterr()
    assert code == 2
    assert "failed" in captured.err

    common.print_warnings(["w1", "w2"])
    output = capsys.readouterr().out
    assert "WARNING: w1" in output
    assert "WARNING: w2" in output
