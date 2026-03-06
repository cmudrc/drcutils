"""CLI entrypoint for bootstrap and permutation statistical utilities."""

from __future__ import annotations

import argparse
from pathlib import Path

from drcutils.cli._common import build_parser, print_error, print_json, read_csv
from drcutils.stats import bootstrap_ci, permutation_test


def _build_parser() -> argparse.ArgumentParser:
    parser = build_parser(
        prog="drc-stats",
        description="Run bootstrap confidence intervals and permutation tests from CSV inputs.",
    )
    sub = parser.add_subparsers(dest="command", required=True, help="Statistical utility command.")

    boot = sub.add_parser(
        "bootstrap-ci",
        help="Run bootstrap confidence interval analysis.",
        description="Compute a bootstrap confidence interval for one CSV column.",
    )
    boot.add_argument("--input", required=True, help="Input CSV file.")
    boot.add_argument("--column", required=True, help="Column name to bootstrap.")
    boot.add_argument(
        "--stat",
        default="mean",
        help="Statistic: mean or median.",
    )
    boot.add_argument("--ci", type=float, default=0.95, help="Confidence level in (0, 1).")
    boot.add_argument("--seed", type=int, default=0, help="Random seed.")

    perm = sub.add_parser(
        "perm-test",
        help="Run two-sample permutation test.",
        description="Compare two CSV columns with a two-sample permutation test.",
    )
    perm.add_argument("--input", required=True, help="Input CSV file.")
    perm.add_argument("--xcol", required=True, help="Column name for sample x.")
    perm.add_argument("--ycol", required=True, help="Column name for sample y.")
    perm.add_argument("--seed", type=int, default=0, help="Random seed.")

    return parser


def main() -> int:
    """Run the stats CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    data_path = Path(args.input)
    try:
        df = read_csv(data_path)
    except ValueError as exc:
        return print_error(str(exc))

    if args.command == "bootstrap-ci":
        if args.column not in df.columns:
            return print_error(f"Column '{args.column}' not found in {data_path}.")
        try:
            result = bootstrap_ci(
                df[args.column].to_numpy(),
                stat=args.stat,
                ci=args.ci,
                seed=args.seed,
            )
        except (ValueError, ImportError) as exc:
            return print_error(str(exc))
    else:
        if args.xcol not in df.columns or args.ycol not in df.columns:
            return print_error(
                f"Columns '{args.xcol}' and/or '{args.ycol}' not found in {data_path}."
            )
        try:
            result = permutation_test(
                df[args.xcol].to_numpy(),
                df[args.ycol].to_numpy(),
                seed=args.seed,
            )
        except (ValueError, ImportError) as exc:
            return print_error(str(exc))

    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
