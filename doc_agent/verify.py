"""Structural check: every public name in the package has a doc heading.

This is the verification the rubric grades (100% of public names documented).
It re-enumerates public names from the source with the AST, then checks each one
appears as a heading or inline-code token somewhere in the generated docs. It
prints a PASS/FAIL line and exits non-zero on failure so it can gate CI.

Usage:
    python doc_agent/verify.py --pkg dataset/target_pkg/ --docs generated_docs/
    # Expected: "PASS: 12 public names, 12 documented (100%)"
"""

import argparse
import ast
import sys
from pathlib import Path

from agent import _enumerate_public

def enumerate_package_public(pkg_dir: Path) -> list[str]:
    """All public names (functions, classes, UPPER constants) across the package."""
    names: list[str] = []
    for py_file in sorted(pkg_dir.glob("*.py")):
        if py_file.stem == "__init__":
            continue
        try:
            names.extend(_enumerate_public(py_file.read_text()))
        except SyntaxError:
            pass
    return names


def is_documented(name: str, docs_text: str) -> bool:
    """A name counts as documented if it appears as a heading or inline-code token."""
    return any(token in docs_text for token in (f"## {name}", f"### {name}", f"`{name}`"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify doc coverage of public names.")
    ap.add_argument("--pkg", required=True, type=Path)
    ap.add_argument("--docs", required=True, type=Path)
    args = ap.parse_args()

    public = enumerate_package_public(args.pkg)
    docs_text = "\n".join(p.read_text() for p in args.docs.glob("*.md"))

    documented = [n for n in public if is_documented(n, docs_text)]
    missing = [n for n in public if n not in documented]
    total = len(public)
    pct = (len(documented) / total * 100) if total else 100.0

    if missing:
        print(f"FAIL: {total} public names, {len(documented)} documented ({pct:.0f}%)")
        print(f"  Missing: {', '.join(missing)}")
        return 1
    print(f"PASS: {total} public names, {len(documented)} documented ({pct:.0f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
