"""CLI entrypoint for bootstrap and permutation statistical utilities."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from drcutils.stats import bootstrap_ci, permutation_test


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run drcutils statistical utilities.")
    sub = parser.add_subparsers(dest="command", required=True)

    boot = sub.add_parser("bootstrap-ci", help="Run bootstrap confidence interval analysis.")
    boot.add_argument("--input", required=True)
    boot.add_argument("--column", required=True)
    boot.add_argument("--stat", default="mean")
    boot.add_argument("--ci", type=float, default=0.95)
    boot.add_argument("--seed", type=int, default=0)

    perm = sub.add_parser("perm-test", help="Run two-sample permutation test.")
    perm.add_argument("--input", required=True)
    perm.add_argument("--xcol", required=True)
    perm.add_argument("--ycol", required=True)
    perm.add_argument("--seed", type=int, default=0)

    return parser


def main() -> int:
    """Run the stats CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    data_path = Path(args.input)
    df = pd.read_csv(data_path)

    if args.command == "bootstrap-ci":
        if args.column not in df.columns:
            raise SystemExit(f"Column '{args.column}' not found in {data_path}.")
        result = bootstrap_ci(
            df[args.column].to_numpy(), stat=args.stat, ci=args.ci, seed=args.seed
        )
    else:
        if args.xcol not in df.columns or args.ycol not in df.columns:
            raise SystemExit(
                f"Columns '{args.xcol}' and/or '{args.ycol}' not found in {data_path}."
            )
        result = permutation_test(
            df[args.xcol].to_numpy(), df[args.ycol].to_numpy(), seed=args.seed
        )

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
