from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

import drcutils.brand as brand


def test_watermark_preserves_alpha_for_rgba_inputs(tmp_path: Path) -> None:
    source_path = tmp_path / "source.png"
    logo_path = tmp_path / "logo.png"
    out_path = tmp_path / "out.png"

    source = Image.new("RGBA", (120, 80), (0, 0, 0, 0))
    source.paste((30, 30, 30, 255), (0, 0, 60, 40))
    source.save(source_path)

    logo = Image.new("RGBA", (30, 10), (255, 255, 255, 160))
    logo.save(logo_path)

    brand.watermark(
        source_path,
        output_filepath=out_path,
        watermark_filepath=logo_path,
        box=[0.05, 0.05, 0.25, None],
    )

    output = Image.open(out_path)
    assert output.mode == "RGBA"
    assert output.getpixel((119, 79))[3] == 0


def test_watermark_auto_on_black_selects_on_black_logo(monkeypatch, tmp_path: Path) -> None:
    source_path = tmp_path / "dark.png"
    out_path = tmp_path / "out.png"
    Image.new("RGB", (200, 120), (5, 5, 5)).save(source_path)

    calls: list[bool] = []
    original = brand.get_logo_path

    def _tracked_get_logo_path(
        layout: str, variant: str, on_black: bool = False, fmt: str = "png"
    ) -> str:
        calls.append(on_black)
        return original(layout, variant, on_black=on_black, fmt=fmt)

    monkeypatch.setattr(brand, "get_logo_path", _tracked_get_logo_path)

    brand.watermark(
        source_path,
        output_filepath=out_path,
        logo_layout="stacked",
        logo_variant="auto",
        on_black="auto",
        box=[0.0, 0.0, 0.2, None],
    )

    assert out_path.exists()
    assert True in calls


@pytest.mark.parametrize(
    "box",
    [
        [0.0, 0.0, 1.2, None],
        [0.0, 0.0, -0.1, None],
        [-0.1, 0.0, 0.2, None],
        [0.0, 1.2, 0.2, None],
        [0.0, 0.0, 0.2],
        [None, 0.0, 0.2, None],
    ],
)
def test_watermark_box_validation_raises(box, tmp_path: Path) -> None:
    source_path = tmp_path / "source.png"
    Image.new("RGB", (20, 20), (255, 255, 255)).save(source_path)

    with pytest.raises(ValueError):
        brand.watermark(source_path, box=box)
