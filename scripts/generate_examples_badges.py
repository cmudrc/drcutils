"""Generate examples status and API coverage badges."""

from __future__ import annotations

import json
from pathlib import Path

METRICS_JSON = Path("artifacts/examples/examples_metrics.json")
EXAMPLES_BADGE_SVG = Path(".github/badges/examples-passing.svg")
API_COVERAGE_BADGE_SVG = Path(".github/badges/examples-api-coverage.svg")


def _pick_color(percent: int) -> str:
    if percent >= 90:
        return "#4c1"
    if percent >= 80:
        return "#97ca00"
    if percent >= 70:
        return "#a4a61d"
    if percent >= 60:
        return "#dfb317"
    if percent >= 50:
        return "#fe7d37"
    return "#e05d44"


def _text_width(text: str) -> int:
    return 10 + (len(text) * 6)


def _render_badge(label: str, message: str, color: str) -> str:
    label_width = _text_width(label)
    message_width = _text_width(message)
    total_width = label_width + message_width
    label_x = label_width / 2
    message_x = label_width + (message_width / 2)

    return f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{total_width}\" height=\"20\" role=\"img\" aria-label=\"{label}: {message}\">\n  <linearGradient id=\"g\" x2=\"0\" y2=\"100%\">\n    <stop offset=\"0\" stop-color=\"#fff\" stop-opacity=\".7\"/>\n    <stop offset=\".1\" stop-color=\"#aaa\" stop-opacity=\".1\"/>\n    <stop offset=\".9\" stop-opacity=\".3\"/>\n    <stop offset=\"1\" stop-opacity=\".5\"/>\n  </linearGradient>\n  <clipPath id=\"r\">\n    <rect width=\"{total_width}\" height=\"20\" rx=\"3\" fill=\"#fff\"/>\n  </clipPath>\n  <g clip-path=\"url(#r)\">\n    <rect width=\"{label_width}\" height=\"20\" fill=\"#555\"/>\n    <rect x=\"{label_width}\" width=\"{message_width}\" height=\"20\" fill=\"{color}\"/>\n    <rect width=\"{total_width}\" height=\"20\" fill=\"url(#g)\"/>\n  </g>\n  <g fill=\"#fff\" text-anchor=\"middle\" font-family=\"Verdana,Geneva,DejaVu Sans,sans-serif\" font-size=\"11\">\n    <text x=\"{label_x:.1f}\" y=\"15\" fill=\"#010101\" fill-opacity=\".3\">{label}</text>\n    <text x=\"{label_x:.1f}\" y=\"14\">{label}</text>\n    <text x=\"{message_x:.1f}\" y=\"15\" fill=\"#010101\" fill-opacity=\".3\">{message}</text>\n    <text x=\"{message_x:.1f}\" y=\"14\">{message}</text>\n  </g>\n</svg>\n"""


def main() -> None:
    """Generate and write examples-status and API-coverage badges."""
    payload = json.loads(METRICS_JSON.read_text(encoding="utf-8"))
    examples = payload["examples"]
    public_api = payload["public_api"]

    passed = int(examples["passed"])
    total = int(examples["total"])
    pass_percent = int(round(float(examples["pass_percent"])))

    covered = int(public_api["covered_exports"])
    exports = int(public_api["total_exports"])
    api_percent = int(round(float(public_api["coverage_percent"])))

    examples_badge = _render_badge(
        "Examples Passing", f"{passed}/{total}", _pick_color(pass_percent)
    )
    api_badge = _render_badge(
        "Example API Coverage", f"{covered}/{exports}", _pick_color(api_percent)
    )

    EXAMPLES_BADGE_SVG.parent.mkdir(parents=True, exist_ok=True)
    EXAMPLES_BADGE_SVG.write_text(examples_badge, encoding="utf-8")
    API_COVERAGE_BADGE_SVG.write_text(api_badge, encoding="utf-8")
    print(f"Wrote {EXAMPLES_BADGE_SVG} and {API_COVERAGE_BADGE_SVG}")


if __name__ == "__main__":
    main()
