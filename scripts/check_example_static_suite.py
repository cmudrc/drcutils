"""Hard-fail static checks for drcutils examples."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = REPO_ROOT / "examples"
_MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _check_notebooks() -> list[str]:
    errors: list[str] = []
    notebooks = sorted(EXAMPLES_ROOT.rglob("*.ipynb"))
    if not notebooks:
        errors.append("No example notebooks found.")
        return errors

    for nb in notebooks:
        try:
            payload = json.loads(nb.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{nb}: invalid JSON ({exc})")
            continue
        if "cells" not in payload:
            errors.append(f"{nb}: missing 'cells' key")
            continue

        for cell in payload.get("cells", []):
            if cell.get("cell_type") != "markdown":
                continue
            source = cell.get("source", [])
            text = "".join(source) if isinstance(source, list) else str(source)
            for link in _MD_LINK_RE.findall(text):
                if "://" in link or link.startswith("#"):
                    continue
                target = (nb.parent / link).resolve()
                if not target.exists():
                    errors.append(f"{nb}: broken local markdown link -> {link}")
    return errors


def _check_python_examples() -> list[str]:
    errors: list[str] = []
    for py_file in sorted(EXAMPLES_ROOT.rglob("*.py")):
        try:
            source = py_file.read_text(encoding="utf-8")
            ast.parse(source, filename=str(py_file))
        except SyntaxError as exc:
            errors.append(f"{py_file}: syntax error ({exc})")
    return errors


def main() -> int:
    """Run static validation for examples and return process exit code."""
    errors = _check_notebooks() + _check_python_examples()
    if errors:
        print("Static example suite failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Static example suite passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
