"""CLI entrypoint for DOE response analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from drcutils.doe import analyze_doe_response


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a DOE response table.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--response-col", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--factor-cols", default=None)
    parser.add_argument("--include-interactions", action="store_true")
    parser.add_argument("--alpha", type=float, default=0.05)
    return parser


def main() -> int:
    """Run the DOE analysis CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    df = pd.read_csv(Path(args.input))
    factor_columns = None
    if args.factor_cols:
        factor_columns = [
            column.strip() for column in args.factor_cols.split(",") if column.strip()
        ]

    result = analyze_doe_response(
        df,
        response=args.response_col,
        factor_columns=factor_columns,
        include_interactions=args.include_interactions,
        alpha=args.alpha,
    )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result["main_effects"].to_csv(out_dir / "main_effects.csv", index=False)
    model_summary = None
    if result["model"] is not None:
        result["model"]["coefficients"].to_csv(out_dir / "coefficients.csv", index=False)
        model_summary = result["model"]["model_summary"]

    summary_payload = {
        "summary": result["summary"],
        "warnings": result["warnings"],
        "interpretation": result["interpretation"],
        "model_summary": model_summary,
    }
    with (out_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary_payload, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print(result["interpretation"])
    print(f"Wrote analysis to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
