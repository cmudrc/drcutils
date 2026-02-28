"""Validate example pass rate and public API coverage thresholds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

EXAMPLE_PASS_THRESHOLD = 100.0
PUBLIC_API_COVERAGE_THRESHOLD = 15.0


def main() -> int:
    """Run example threshold checks and return process exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics-json", required=True)
    args = parser.parse_args()

    path = Path(args.metrics_json)
    if not path.exists():
        raise FileNotFoundError(f"Examples metrics JSON not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))
    examples = payload.get("examples", {})
    public_api = payload.get("public_api", {})

    pass_percent = float(examples.get("pass_percent", 0.0))
    api_percent = float(public_api.get("coverage_percent", 0.0))

    print(f"Example pass rate: {pass_percent:.1f}% (threshold {EXAMPLE_PASS_THRESHOLD:.1f}%)")
    if pass_percent < EXAMPLE_PASS_THRESHOLD:
        print("Example pass-rate threshold failed.")
        return 1

    print(
        f"Example API coverage: {api_percent:.1f}% (threshold {PUBLIC_API_COVERAGE_THRESHOLD:.1f}%)"
    )
    if api_percent < PUBLIC_API_COVERAGE_THRESHOLD:
        print("Example API coverage threshold failed.")
        return 1

    print("Example thresholds passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
