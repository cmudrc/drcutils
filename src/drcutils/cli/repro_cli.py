"""CLI entrypoint for reproducibility snapshots."""

from __future__ import annotations

import argparse

from drcutils.cli._common import (
    build_parser,
    parse_json_argument,
    print_error,
    print_warnings,
)
from drcutils.runtime import capture_run_context, write_run_manifest


def _build_parser() -> argparse.ArgumentParser:
    parser = build_parser(
        prog="drc-repro",
        description="Capture reproducibility snapshots for data and script runs.",
    )
    sub = parser.add_subparsers(dest="command", required=True, help="Reproducibility command.")

    snapshot = sub.add_parser(
        "snapshot",
        help="Write a JSON run-context manifest.",
        description="Capture environment, git, and input metadata to a JSON manifest.",
    )
    snapshot.add_argument("--out", required=True, help="Output path for the JSON manifest.")
    snapshot.add_argument("--seed", type=int, default=None, help="Optional random seed metadata.")
    snapshot.add_argument(
        "--input",
        action="append",
        dest="inputs",
        default=None,
        help="Input file path to hash. Repeat for multiple files.",
    )
    snapshot.add_argument(
        "--extra-json",
        default=None,
        help="Optional JSON object for additional structured metadata.",
    )
    return parser


def main() -> int:
    """Run the reproducibility CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    extra = None
    if args.extra_json is not None:
        try:
            parsed = parse_json_argument(args.extra_json, label="--extra-json")
        except ValueError as exc:
            return print_error(str(exc))
        if not isinstance(parsed, dict):
            return print_error("--extra-json must decode to a JSON object.")
        extra = parsed

    try:
        context = capture_run_context(seed=args.seed, input_paths=args.inputs, extra=extra)
        out_path = write_run_manifest(context, args.out)
    except (FileNotFoundError, OSError, ValueError) as exc:
        return print_error(str(exc))

    print(out_path)
    print_warnings(context["warnings"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
