"""Shared helpers for drcutils command-line interfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

_CSV_PARSE_ERRORS: tuple[type[Exception], ...] = (pd.errors.EmptyDataError, pd.errors.ParserError)


def build_parser(*, prog: str, description: str) -> argparse.ArgumentParser:
    """Build an argument parser with consistent CLI formatting defaults."""
    return argparse.ArgumentParser(
        prog=prog,
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )


def parse_json_argument(raw_json: str, *, label: str) -> Any:
    """Decode JSON passed on the command line."""
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid {label}: {exc}") from exc


def parse_json_object(raw_json: str, *, label: str) -> dict[str, Any]:
    """Decode a JSON object passed on the command line."""
    loaded = parse_json_argument(raw_json, label=label)
    if not isinstance(loaded, dict):
        raise ValueError(f"{label} must decode to a JSON object.")
    return loaded


def parse_json_list(raw_json: str, *, label: str) -> list[Any]:
    """Decode a JSON list passed on the command line."""
    loaded = parse_json_argument(raw_json, label=label)
    if not isinstance(loaded, list):
        raise ValueError(f"{label} must decode to a JSON list.")
    return loaded


def read_json_file(path: Path, *, label: str) -> Any:
    """Load JSON from disk."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{label} not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid {label} '{path}': {exc}") from exc


def write_json_file(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON to disk with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV input path with user-facing error messages."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError as exc:
        raise ValueError(f"Input CSV not found: {path}") from exc
    except _CSV_PARSE_ERRORS as exc:
        raise ValueError(f"Failed to parse CSV '{path}': {exc}") from exc


def parse_comma_list(raw_value: str | None) -> list[str] | None:
    """Split a comma-separated CLI argument into a clean list."""
    if raw_value is None:
        return None
    values = [item.strip() for item in raw_value.split(",") if item.strip()]
    return values or None


def print_json(payload: dict[str, Any]) -> None:
    """Print JSON to stdout in a predictable format."""
    print(json.dumps(payload, indent=2, sort_keys=True))


def print_error(message: str) -> int:
    """Print a user-facing CLI error and return an error exit code."""
    print(message, file=sys.stderr)
    return 2
