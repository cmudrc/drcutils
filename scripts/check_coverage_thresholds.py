"""Validate line coverage against drcutils thresholds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

GLOBAL_THRESHOLD = 59.0


def main() -> int:
    """Run coverage threshold checks and return process exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage-json", required=True)
    args = parser.parse_args()

    path = Path(args.coverage_json)
    if not path.exists():
        raise FileNotFoundError(f"Coverage JSON not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))
    totals = payload.get("totals", {})
    percent = float(totals.get("percent_covered", totals.get("percent_covered_display", 0.0)))

    print(f"Global line coverage: {percent:.2f}% (threshold {GLOBAL_THRESHOLD:.2f}%)")
    if percent < GLOBAL_THRESHOLD:
        print("Coverage threshold failed.")
        return 1
    print("Coverage threshold passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
