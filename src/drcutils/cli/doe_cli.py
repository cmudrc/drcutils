"""CLI entrypoint for DOE generation."""

from __future__ import annotations

import argparse
from pathlib import Path

from drcutils.cli._common import (
    build_parser,
    parse_json_object,
    print_error,
    print_warnings,
    write_csv_file,
)
from drcutils.doe import generate_doe


def _build_parser() -> argparse.ArgumentParser:
    parser = build_parser(
        prog="drc-doe",
        description="Generate design-of-experiments (DOE) run tables.",
    )
    parser.add_argument(
        "--kind",
        required=True,
        choices=["full", "lhs", "frac2"],
        help="Design type to generate.",
    )
    parser.add_argument(
        "--factors-json",
        required=True,
        help="JSON object mapping factor names to definitions.",
    )
    parser.add_argument(
        "--n-samples",
        type=int,
        default=None,
        help="Number of LHS samples (required for --kind lhs).",
    )
    parser.add_argument("--seed", type=int, default=0, help="Random seed for run ordering.")
    parser.add_argument(
        "--center-points",
        type=int,
        default=0,
        help="Number of center points to append to the generated design.",
    )
    parser.add_argument(
        "--replicates",
        type=int,
        default=1,
        help="Number of full-design replicates to include.",
    )
    parser.add_argument("--out", required=True, help="Output CSV path for the design table.")
    randomize_group = parser.add_mutually_exclusive_group()
    randomize_group.add_argument(
        "--randomize",
        dest="randomize",
        action="store_true",
        help="Randomize run order after generation.",
    )
    randomize_group.add_argument(
        "--no-randomize",
        dest="randomize",
        action="store_false",
        help="Keep generated run order unchanged.",
    )
    parser.set_defaults(randomize=True)
    return parser


def main() -> int:
    """Run the DOE CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    try:
        factors = parse_json_object(args.factors_json, label="--factors-json")
        result = generate_doe(
            kind=args.kind,
            factors=factors,
            n_samples=args.n_samples,
            seed=args.seed,
            center_points=args.center_points,
            replicates=args.replicates,
            randomize=args.randomize,
        )
    except (ValueError, ImportError) as exc:
        return print_error(str(exc))

    out_path = Path(args.out)
    try:
        write_csv_file(out_path, result["design"])
    except ValueError as exc:
        return print_error(str(exc))

    print(result["interpretation"])
    print_warnings(result["warnings"])
    print(f"Wrote design to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
