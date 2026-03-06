from __future__ import annotations

import tomllib
from importlib.resources import files
from pathlib import Path


def test_package_data_contains_curated_brand_asset_patterns() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    patterns = pyproject["tool"]["setuptools"]["package-data"]["drcutils"]

    expected = {
        "data/brand_assets/logos/horizontal/*.png",
        "data/brand_assets/logos/stacked/*.png",
        "data/brand_assets/logos/symbol/*.png",
        "data/brand_assets/logos/on_black/*.png",
        "data/brand_assets/patterns/*.png",
        "data/brand_assets/gradients/*.png",
        "data/brand_assets/circles/*.png",
        "data/brand_assets/scribbles/thin/*.png",
        "data/brand_assets/scribbles/thick/*.png",
    }
    assert expected.issubset(set(patterns))


def test_package_data_excludes_icon_bulk() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    patterns = pyproject["tool"]["setuptools"]["package-data"]["drcutils"]
    assert all("icons" not in pattern.lower() for pattern in patterns)


def test_curated_assets_exist_under_package_data_root() -> None:
    data_root = files("drcutils") / "data" / "brand_assets"

    required = [
        data_root / "logos" / "horizontal" / "full.png",
        data_root / "logos" / "on_black" / "stacked.png",
        data_root / "patterns" / "grey.png",
        data_root / "gradients" / "01.png",
        data_root / "circles" / "blue.png",
        data_root / "scribbles" / "thick" / "red.png",
    ]
    for path in required:
        assert path.is_file()
