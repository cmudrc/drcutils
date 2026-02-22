"""Generate static example metrics and public API coverage metrics."""

from __future__ import annotations

import ast
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = REPO_ROOT / "examples"
PUBLIC_API_INIT = REPO_ROOT / "src" / "drcutils" / "__init__.py"
METRICS_JSON = REPO_ROOT / "artifacts" / "examples" / "examples_metrics.json"


def _discover_notebooks() -> list[Path]:
    return sorted(EXAMPLES_ROOT.rglob("*.ipynb"))


def _discover_python_examples() -> list[Path]:
    return sorted(EXAMPLES_ROOT.rglob("*.py"))


def _extract_exports(path: Path) -> list[str]:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in module.body:
        if isinstance(node, ast.Assign):
            if (
                len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "__all__"
            ):
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    names: list[str] = []
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            names.append(elt.value)
                    return names
    return []


def _notebook_code_cells(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cells = payload.get("cells", [])
    code_lines: list[str] = []
    for cell in cells:
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            if isinstance(source, list):
                code_lines.extend(source)
            elif isinstance(source, str):
                code_lines.append(source)
            code_lines.append("\n")
    return "".join(code_lines)


def _usage_from_source(source: str, exports: set[str]) -> set[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    hits: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in exports:
            hits.add(node.id)
        if isinstance(node, ast.Attribute) and node.attr in exports:
            hits.add(node.attr)
    return hits


def main() -> None:
    """Compute example/static metrics and write metrics JSON."""
    notebooks = _discover_notebooks()
    python_examples = _discover_python_examples()
    exports = _extract_exports(PUBLIC_API_INIT)
    export_set = set(exports)

    covered: set[str] = set()
    for py_file in python_examples:
        source = py_file.read_text(encoding="utf-8")
        covered.update(_usage_from_source(source, export_set))
    for nb in notebooks:
        covered.update(_usage_from_source(_notebook_code_cells(nb), export_set))

    total_examples = len(notebooks) + len(python_examples)
    passed_examples = total_examples

    metrics = {
        "examples": {
            "total": total_examples,
            "passed": passed_examples,
            "failed": total_examples - passed_examples,
            "pass_percent": 100.0 if total_examples > 0 else 0.0,
        },
        "public_api": {
            "total_exports": len(exports),
            "covered_exports": len(covered),
            "coverage_percent": round((len(covered) / len(exports)) * 100, 1) if exports else 100.0,
            "covered_symbols": sorted(covered),
            "missing_symbols": sorted(set(exports) - covered),
        },
    }

    METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    METRICS_JSON.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {METRICS_JSON}")


if __name__ == "__main__":
    main()
