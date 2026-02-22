"""CLI entrypoint for DOE generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from drcutils.doe.one_stop import generate_doe


def main() -> int:
    """Run the DOE CLI."""
    parser = argparse.ArgumentParser(description="Generate DOE tables.")
    parser.add_argument("--kind", required=True, choices=["full", "lhs", "frac2"])
    parser.add_argument(
        "--factors-json", required=True, help="JSON mapping for factor definitions."
    )
    parser.add_argument("--n-samples", type=int, default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", required=True, help="Output CSV path.")
    args = parser.parse_args()

    try:
        factors = json.loads(args.factors_json)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid --factors-json: {exc}") from exc

    result = generate_doe(
        kind=args.kind,
        factors=factors,
        n_samples=args.n_samples,
        seed=args.seed,
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    result["design"].to_csv(out_path, index=False)
    print(result["interpretation"])
    print(f"Wrote design to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
