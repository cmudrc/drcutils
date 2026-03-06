"""CLI entrypoint for dataset utilities."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from drcutils.cli._common import (
    build_parser,
    parse_json_object,
    print_error,
    print_json,
    read_csv,
    read_json_file,
    write_json_file,
)
from drcutils.data import generate_codebook, profile_dataframe, validate_dataframe


def _load_schema(args: argparse.Namespace) -> dict[str, object]:
    """Load schema constraints for ``validate`` commands."""
    if args.schema_json is not None:
        return parse_json_object(args.schema_json, label="--schema-json")

    schema_path = Path(args.schema_file)
    loaded = read_json_file(schema_path, label="Schema file")
    if not isinstance(loaded, dict):
        raise ValueError("Schema file must decode to a JSON object.")
    return loaded


def _load_descriptions(raw_json: str | None) -> dict[str, str] | None:
    """Load optional codebook descriptions."""
    if raw_json is None:
        return None
    loaded = parse_json_object(raw_json, label="--descriptions-json")
    return {str(key): str(value) for key, value in loaded.items()}


def _build_parser() -> argparse.ArgumentParser:
    parser = build_parser(
        prog="drc-data",
        description="Profile tabular datasets, validate schemas, and generate codebooks.",
    )
    sub = parser.add_subparsers(dest="command", required=True, help="Dataset utility command.")

    profile = sub.add_parser(
        "profile",
        help="Profile a CSV file.",
        description="Profile a CSV file and report column-level diagnostics.",
    )
    profile.add_argument("--input", required=True, help="Input CSV file to profile.")
    profile.add_argument("--out", default=None, help="Optional JSON output path.")
    profile.add_argument(
        "--max-categorical-levels",
        type=int,
        default=20,
        help="Warn when non-numeric columns exceed this unique-value count.",
    )

    validate = sub.add_parser(
        "validate",
        help="Validate a CSV file against a schema.",
        description="Validate a CSV file against a declarative JSON schema.",
    )
    validate.add_argument("--input", required=True, help="Input CSV file to validate.")
    schema_group = validate.add_mutually_exclusive_group(required=True)
    schema_group.add_argument(
        "--schema-json",
        default=None,
        help="Inline JSON schema object.",
    )
    schema_group.add_argument(
        "--schema-file",
        default=None,
        help="Path to a JSON schema file.",
    )
    validate.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Return a non-zero exit code when warnings are present.",
    )

    codebook = sub.add_parser(
        "codebook",
        help="Generate a CSV codebook.",
        description="Generate a compact codebook for a CSV file.",
    )
    codebook.add_argument("--input", required=True, help="Input CSV file for codebook generation.")
    codebook.add_argument("--out", required=True, help="Output CSV path for the codebook.")
    codebook.add_argument(
        "--descriptions-json",
        default=None,
        help="Optional JSON object that maps column names to descriptions.",
    )

    return parser


def main() -> int:
    """Run the dataset CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    try:
        df = read_csv(Path(args.input))
    except ValueError as exc:
        return print_error(str(exc))

    if args.command == "profile":
        result = profile_dataframe(
            df,
            max_categorical_levels=args.max_categorical_levels,
        )
        if args.out:
            write_json_file(Path(args.out), result)
        else:
            print_json(result)
        return 0

    if args.command == "validate":
        try:
            result = validate_dataframe(df, _load_schema(args))
        except ValueError as exc:
            return print_error(str(exc))
        print_json(result)
        if result["errors"]:
            return 2
        if result["warnings"] and args.fail_on_warning:
            return 3
        return 0

    try:
        descriptions = _load_descriptions(args.descriptions_json)
        codebook = generate_codebook(df, descriptions=descriptions)
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        codebook.to_csv(out_path, index=False)
    except ValueError as exc:
        return print_error(str(exc))
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"Wrote codebook to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
