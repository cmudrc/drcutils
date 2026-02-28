from __future__ import annotations

import pandas as pd
import pytest

from drcutils.data import convert


def test_convert_csv_to_json_roundtrip(tmp_path) -> None:
    src = tmp_path / "source.csv"
    dst = tmp_path / "target.json"
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    df.to_csv(src, index=False)

    convert(src, dst)

    restored = pd.read_json(dst)
    assert list(restored["a"]) == [1, 2]
    assert list(restored["b"]) == ["x", "y"]


def test_convert_invalid_source_extension_raises(tmp_path) -> None:
    src = tmp_path / "source.invalid"
    dst = tmp_path / "target.json"
    src.write_text("x", encoding="utf-8")

    with pytest.raises(ValueError, match="cannot be opened"):
        convert(src, dst)


def test_convert_invalid_target_extension_raises(tmp_path) -> None:
    src = tmp_path / "source.csv"
    dst = tmp_path / "target.invalid"
    src.write_text("a\n1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="cannot be written"):
        convert(src, dst)


def test_convert_non_convertible_pair_raises(tmp_path) -> None:
    src = tmp_path / "source.png"
    dst = tmp_path / "target.csv"
    src.write_bytes(b"not-an-image")

    with pytest.raises(ValueError, match="cannot be converted"):
        convert(src, dst)
