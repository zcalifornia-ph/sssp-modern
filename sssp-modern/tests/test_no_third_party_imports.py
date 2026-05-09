from __future__ import annotations

import ast
import sys
from pathlib import Path

ALLOWED_IMPORT_ROOTS = set(sys.stdlib_module_names) | {"sssp"}


def test_src_sssp_imports_are_stdlib_or_local() -> None:
    source_root = Path(__file__).resolve().parents[1] / "src" / "sssp"
    unexpected: list[str] = []

    for path in sorted(source_root.rglob("*.py")):
        for root in _import_roots(path):
            if root not in ALLOWED_IMPORT_ROOTS:
                relative = path.relative_to(source_root.parent)
                unexpected.append(f"{relative}: {root}")

    assert unexpected == []


def _import_roots(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.extend(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                roots.append(node.module.split(".", 1)[0])

    return tuple(roots)
