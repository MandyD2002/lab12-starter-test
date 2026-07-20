"""Generate API docs from a Python package (HKBU GenAI Version).

Usage:
    python doc_agent/agent.py --pkg dataset/target_pkg/ --out generated_docs/
"""

import argparse
import ast
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- HKBU GPT API Configuration ---
API_KEY = os.getenv("HKBU_API_KEY")
BASE_URL = "https://genai.hkbu.edu.hk/api/v0/rest"
MODEL_NAME = "gpt-4.1"
API_VERSION = "2024-12-01-preview"

DOC_SYSTEM = """\
You write API reference documentation. Given a Python source file, produce
Markdown documentation with:

- One ## heading per public function, class, or constant.
- For each function: a one-paragraph description, "Parameters" subsection
  with types and meanings, "Returns" subsection, and "Example" subsection
  with runnable code.

Rules:
- Only document PUBLIC names (no leading underscore).
- Do not invent parameters or return types not in the source.
- Use existing docstrings as ground truth; do not contradict them.
- If a function has no docstring, infer behaviour from the implementation
  but mark the description as "(inferred from implementation)".
"""

def document_file(path: Path) -> str:
    """Generate Markdown docs for one source file, or "" if it has no public names."""
    source = path.read_text()
    public = _enumerate_public(source)
    if not public:
        return ""

    # HKBU API Payload
    url = f"{BASE_URL}/deployments/{MODEL_NAME}/chat/completions?api-version={API_VERSION}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": DOC_SYSTEM},
            {"role": "user", "content": (
                "PUBLIC NAMES (these are the only things you should document):\n"
                f"{', '.join(public)}\n\n"
                f"SOURCE:\n```python\n{source}\n```"
            )}
        ],
        "temperature": 0.3,
        "max_tokens": 4096,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"Error generating docs: {str(e)}"


def _enumerate_public(source: str) -> list[str]:
    """Top-level public functions, classes, and UPPER_CASE constants."""
    tree = ast.parse(source)
    public: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                public.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if (isinstance(target, ast.Name) and not target.id.startswith("_")
                        and target.id.isupper()):
                    public.append(target.id)
    return public


def document_package(pkg_dir: Path, out_dir: Path) -> None:
    """Document every non-dunder .py file in pkg_dir into out_dir/<stem>.md."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for py_file in sorted(pkg_dir.glob("*.py")):
        if py_file.stem == "__init__":
            continue
        doc = document_file(py_file)
        if doc:
            (out_dir / f"{py_file.stem}.md").write_text(doc)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate API docs from a Python package (HKBU version).")
    ap.add_argument("--pkg", required=True, type=Path, help="package directory of .py files")
    ap.add_argument("--out", required=True, type=Path, help="output directory for .md files")
    args = ap.parse_args()
    document_package(args.pkg, args.out)
    print(f"Wrote docs for {args.pkg} into {args.out}")


if __name__ == "__main__":
    main()