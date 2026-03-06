"""CLI entrypoint for DOE response analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

from drcutils.cli._common import (
    build_parser,
    ensure_directory,
    parse_comma_list,
    print_error,
    print_warnings,
    read_csv,
    write_csv_file,
    write_json_file,
)
from drcutils.doe import analyze_doe_response


def _build_parser() -> argparse.ArgumentParser:
    parser = build_parser(
        prog="drc-doe-analyze",
        description="Analyze DOE response data and write tabular diagnostics.",
    )
    parser.add_argument("--input", required=True, help="Input CSV file with DOE responses.")
    parser.add_argument(
        "--response-col",
        required=True,
        help="Name of the response column to analyze.",
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        help="Output directory for generated analysis artifacts.",
    )
    parser.add_argument(
        "--factor-cols",
        default=None,
        help="Optional comma-separated factor columns. Defaults to all non-response columns.",
    )
    parser.add_argument(
        "--include-interactions",
        action="store_true",
        help="Include pairwise interactions in the screening model when possible.",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.05,
        help="Significance threshold for fitted model confidence intervals.",
    )
    return parser


def main() -> int:
    """Run the DOE analysis CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    try:
        df = read_csv(Path(args.input))
        factor_columns = parse_comma_list(args.factor_cols)
        result = analyze_doe_response(
            df,
            response=args.response_col,
            factor_columns=factor_columns,
            include_interactions=args.include_interactions,
            alpha=args.alpha,
        )
    except (ValueError, ImportError) as exc:
        return print_error(str(exc))

    out_dir = Path(args.out_dir)
    try:
        ensure_directory(out_dir, label="output directory")
        write_csv_file(out_dir / "main_effects.csv", result["main_effects"])
        model_summary = None
        if result["model"] is not None:
            write_csv_file(out_dir / "coefficients.csv", result["model"]["coefficients"])
            model_summary = result["model"]["model_summary"]

        summary_payload = {
            "summary": result["summary"],
            "warnings": result["warnings"],
            "interpretation": result["interpretation"],
            "model_summary": model_summary,
        }
        write_json_file(out_dir / "summary.json", summary_payload)
    except ValueError as exc:
        return print_error(str(exc))

    print(result["interpretation"])
    print_warnings(result["warnings"])
    print(f"Wrote analysis to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
