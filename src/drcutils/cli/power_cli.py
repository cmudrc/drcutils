"""CLI entrypoint for power-analysis utilities."""

from __future__ import annotations

import argparse
from pathlib import Path

from drcutils.cli._common import (
    build_parser,
    parse_json_list,
    print_error,
    print_json,
)
from drcutils.stats import estimate_sample_size, minimum_detectable_effect, power_curve


def _build_parser() -> argparse.ArgumentParser:
    parser = build_parser(
        prog="drc-power",
        description="Estimate sample size, power curves, and minimum detectable effects.",
    )
    sub = parser.add_subparsers(dest="command", required=True, help="Power analysis command.")

    sample = sub.add_parser(
        "sample-size",
        help="Estimate sample size.",
        description="Estimate a total sample size for a supported t-test family.",
    )
    sample.add_argument("--test", required=True, help="Supported test family.")
    sample.add_argument("--effect-size", required=True, type=float, help="Target Cohen's d.")
    sample.add_argument("--alpha", type=float, default=0.05, help="Significance level.")
    sample.add_argument("--power", type=float, default=0.8, help="Target statistical power.")
    sample.add_argument("--ratio", type=float, default=1.0, help="Group-size ratio n2/n1.")
    sample.add_argument(
        "--alternative",
        default="two-sided",
        help="Alternative hypothesis: two-sided, larger, or smaller.",
    )

    curve = sub.add_parser(
        "curve",
        help="Write a power curve CSV.",
        description="Compute achieved power over a JSON list of effect sizes.",
    )
    curve.add_argument("--test", required=True, help="Supported test family.")
    curve.add_argument("--n", required=True, type=int, help="Total planned sample size.")
    curve.add_argument(
        "--effect-sizes-json",
        required=True,
        help="JSON list of effect sizes to evaluate.",
    )
    curve.add_argument("--alpha", type=float, default=0.05, help="Significance level.")
    curve.add_argument("--ratio", type=float, default=1.0, help="Group-size ratio n2/n1.")
    curve.add_argument(
        "--alternative",
        default="two-sided",
        help="Alternative hypothesis: two-sided, larger, or smaller.",
    )
    curve.add_argument("--out", required=True, help="Output CSV path for the power curve.")

    mde = sub.add_parser(
        "mde",
        help="Estimate minimum detectable effect.",
        description="Solve for the smallest detectable effect at a fixed sample size.",
    )
    mde.add_argument("--test", required=True, help="Supported test family.")
    mde.add_argument("--n", required=True, type=int, help="Total planned sample size.")
    mde.add_argument("--alpha", type=float, default=0.05, help="Significance level.")
    mde.add_argument("--power", type=float, default=0.8, help="Target statistical power.")
    mde.add_argument("--ratio", type=float, default=1.0, help="Group-size ratio n2/n1.")
    mde.add_argument(
        "--alternative",
        default="two-sided",
        help="Alternative hypothesis: two-sided, larger, or smaller.",
    )
    return parser


def main() -> int:
    """Run the power CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "sample-size":
        try:
            result = estimate_sample_size(
                args.effect_size,
                test=args.test,
                alpha=args.alpha,
                power=args.power,
                ratio=args.ratio,
                alternative=args.alternative,
            )
        except (ValueError, ImportError) as exc:
            return print_error(str(exc))
        print_json(result)
        return 0

    if args.command == "curve":
        try:
            effect_sizes = parse_json_list(args.effect_sizes_json, label="--effect-sizes-json")
            curve = power_curve(
                effect_sizes=list(effect_sizes),
                n=args.n,
                test=args.test,
                alpha=args.alpha,
                ratio=args.ratio,
                alternative=args.alternative,
            )
        except (ValueError, ImportError) as exc:
            return print_error(str(exc))

        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            curve.to_csv(out_path, index=False)
        except OSError as exc:
            return print_error(str(exc))
        print(f"Wrote power curve to {out_path}")
        return 0

    try:
        result = minimum_detectable_effect(
            args.n,
            test=args.test,
            alpha=args.alpha,
            power=args.power,
            ratio=args.ratio,
            alternative=args.alternative,
        )
    except (ValueError, ImportError) as exc:
        return print_error(str(exc))

    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
