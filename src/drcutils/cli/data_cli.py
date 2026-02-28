"""CLI entrypoint for dataset utilities."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

from drcutils.dataset import generate_codebook, profile_dataframe, validate_dataframe


def _write_json(payload: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _load_json_argument(raw_json: str, *, label: str) -> Any:
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid {label}: {exc}") from exc


def _load_schema(args: argparse.Namespace) -> dict[str, Any]:
    if args.schema_json is not None:
        loaded = _load_json_argument(args.schema_json, label="--schema-json")
    else:
        schema_path = Path(args.schema_file)
        try:
            loaded = json.loads(schema_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise SystemExit(f"Schema file not found: {schema_path}") from exc
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid schema file '{schema_path}': {exc}") from exc
    if not isinstance(loaded, dict):
        raise SystemExit("Schema input must decode to a JSON object.")
    return loaded


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run drcutils dataset utilities.")
    sub = parser.add_subparsers(dest="command", required=True)

    profile = sub.add_parser("profile", help="Profile a CSV file.")
    profile.add_argument("--input", required=True)
    profile.add_argument("--out", default=None)
    profile.add_argument("--max-categorical-levels", type=int, default=20)

    validate = sub.add_parser("validate", help="Validate a CSV file against a schema.")
    validate.add_argument("--input", required=True)
    schema_group = validate.add_mutually_exclusive_group(required=True)
    schema_group.add_argument("--schema-json", default=None)
    schema_group.add_argument("--schema-file", default=None)
    validate.add_argument("--fail-on-warning", action="store_true")

    codebook = sub.add_parser("codebook", help="Generate a CSV codebook.")
    codebook.add_argument("--input", required=True)
    codebook.add_argument("--out", required=True)
    codebook.add_argument("--descriptions-json", default=None)

    return parser


def main() -> int:
    """Run the dataset CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    input_path = Path(args.input)
    df = pd.read_csv(input_path)

    if args.command == "profile":
        result = profile_dataframe(
            df,
            max_categorical_levels=args.max_categorical_levels,
        )
        if args.out:
            _write_json(result, Path(args.out))
        else:
            print(result)
        return 0

    if args.command == "validate":
        result = validate_dataframe(df, _load_schema(args))
        print(result)
        if result["errors"]:
            return 2
        if result["warnings"] and args.fail_on_warning:
            return 3
        return 0

    descriptions: dict[str, str] | None = None
    if args.descriptions_json is not None:
        loaded = _load_json_argument(args.descriptions_json, label="--descriptions-json")
        if not isinstance(loaded, dict):
            print("Descriptions must decode to a JSON object.", file=sys.stderr)
            return 2
        descriptions = {str(key): str(value) for key, value in loaded.items()}

    codebook = generate_codebook(df, descriptions=descriptions)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    codebook.to_csv(out_path, index=False)
    print(f"Wrote codebook to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
