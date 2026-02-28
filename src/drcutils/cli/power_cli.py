"""CLI entrypoint for power-analysis utilities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from drcutils.stats import estimate_sample_size, minimum_detectable_effect, power_curve


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run drcutils power-analysis utilities.")
    sub = parser.add_subparsers(dest="command", required=True)

    sample = sub.add_parser("sample-size", help="Estimate sample size.")
    sample.add_argument("--test", required=True)
    sample.add_argument("--effect-size", required=True, type=float)
    sample.add_argument("--alpha", type=float, default=0.05)
    sample.add_argument("--power", type=float, default=0.8)
    sample.add_argument("--ratio", type=float, default=1.0)
    sample.add_argument("--alternative", default="two-sided")

    curve = sub.add_parser("curve", help="Write a power curve CSV.")
    curve.add_argument("--test", required=True)
    curve.add_argument("--n", required=True, type=int)
    curve.add_argument("--effect-sizes-json", required=True)
    curve.add_argument("--alpha", type=float, default=0.05)
    curve.add_argument("--ratio", type=float, default=1.0)
    curve.add_argument("--alternative", default="two-sided")
    curve.add_argument("--out", required=True)

    mde = sub.add_parser("mde", help="Estimate minimum detectable effect.")
    mde.add_argument("--test", required=True)
    mde.add_argument("--n", required=True, type=int)
    mde.add_argument("--alpha", type=float, default=0.05)
    mde.add_argument("--power", type=float, default=0.8)
    mde.add_argument("--ratio", type=float, default=1.0)
    mde.add_argument("--alternative", default="two-sided")
    return parser


def main() -> int:
    """Run the power CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "sample-size":
        result = estimate_sample_size(
            args.effect_size,
            test=args.test,
            alpha=args.alpha,
            power=args.power,
            ratio=args.ratio,
            alternative=args.alternative,
        )
        print(result)
        return 0

    if args.command == "curve":
        try:
            effect_sizes = json.loads(args.effect_sizes_json)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid --effect-sizes-json: {exc}") from exc
        curve = power_curve(
            effect_sizes=list(effect_sizes),
            n=args.n,
            test=args.test,
            alpha=args.alpha,
            ratio=args.ratio,
            alternative=args.alternative,
        )
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        curve.to_csv(out_path, index=False)
        print(f"Wrote power curve to {out_path}")
        return 0

    result = minimum_detectable_effect(
        args.n,
        test=args.test,
        alpha=args.alpha,
        power=args.power,
        ratio=args.ratio,
        alternative=args.alternative,
    )
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
