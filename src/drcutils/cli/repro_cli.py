"""CLI entrypoint for reproducibility snapshots."""

from __future__ import annotations

import argparse
import json
import sys

from drcutils.runtime import capture_run_context, write_run_manifest


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capture drcutils run-context snapshots.")
    sub = parser.add_subparsers(dest="command", required=True)

    snapshot = sub.add_parser("snapshot", help="Write a JSON run-context manifest.")
    snapshot.add_argument("--out", required=True)
    snapshot.add_argument("--seed", type=int, default=None)
    snapshot.add_argument("--input", action="append", dest="inputs", default=None)
    snapshot.add_argument("--extra-json", default=None)
    return parser


def main() -> int:
    """Run the reproducibility CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    extra = None
    if args.extra_json is not None:
        try:
            extra = json.loads(args.extra_json)
        except json.JSONDecodeError as exc:
            print(f"Invalid --extra-json: {exc}", file=sys.stderr)
            return 2

    try:
        context = capture_run_context(seed=args.seed, input_paths=args.inputs, extra=extra)
        out_path = write_run_manifest(context, args.out)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(out_path)
    for warning in context["warnings"]:
        print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
