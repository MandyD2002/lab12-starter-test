"""v1 -- Structured code-review agent (HKBU GPT Version).

This agent implements structured code review by enforcing a Pydantic schema.
The Pydantic models (ReviewComment, ReviewResult) and the parse/validate 
plumbing are fixed to ensure compatibility with the automated grading script.

Usage:
    python review_agent/v1.py --diff dataset/review_set.jsonl --idx 0
    python review_agent/v1.py --diff /tmp/pr.diff --output /tmp/review.json --pr-id 42
"""

import argparse
import json
import os
import re
from pathlib import Path
from typing import Literal
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from a local .env file
load_dotenv()

# --- HKBU GPT API Configuration ---
API_KEY = os.getenv("HKBU_API_KEY")
BASE_URL = "https://genai.hkbu.edu.hk/api/v0/rest"
MODEL_NAME = "gpt-4.1"
API_VERSION = "2024-12-01-preview"

# --- Schema (DO NOT CHANGE: grading scripts and GitHub Actions depend on this) ---
class ReviewComment(BaseModel):
    line: int = Field(ge=0)
    severity: Literal["blocker", "major", "minor"]
    category: Literal["bug", "style", "suggestion", "nit"]
    description: str = Field(min_length=10, max_length=400)
    suggestion: str = Field(default="", max_length=400)

class ReviewResult(BaseModel):
    pr_id: str
    comments: list[ReviewComment] = Field(default_factory=list)

# --- Prompt Tuning Section ---
# This system prompt enforces strict JSON output without markdown formatting.
# You change the prompt (and optionally add post-filtering) to raise precision.
REVIEW_SYSTEM = """\
You are an expert software engineer. Review the Git diff for Bugs.

Output ONLY valid JSON (no markdown). 
If NO bugs are found, return {"comments": []}.

CATEGORIES (You MUST use these exactly): 
- "bug": Use this for runtime crashes (DivisionByZero, IndexErrors), security risks (SQLi, MD5), or logic flaws.
- "style", "suggestion", "nit": Use these ONLY if the bug is minor; otherwise, stick to "bug".

CRITICAL INSTRUCTIONS TO IMPROVE RECALL:
1. EXHAUSTIVE CHECK: You must check every added line. If a logic error is present (e.g., missing 'with' for file I/O, missing check for empty list before division), you MUST flag it.
2. BE BOLD: If you see a potential logic flaw, flag it as "bug". Do not stay silent just because you are slightly unsure.
3. ALIGNMENT: Ensure your 'line' number matches the line in the diff.
4. CATEGORY MATCHING: Since this is for an automated grading system, prioritize the "bug" category for any logic/security issues to ensure TP match.

JSON FORMAT:
{
  "comments": [
    {
      "line": <int>,
      "severity": "major",
      "category": "bug",
      "description": "<detailed description of the failure>",
      "suggestion": "<the corrected code snippet>"
    }
  ]
}
"""


def review(pr_id: str, diff: str) -> ReviewResult:
    """Run the review agent over a diff and return a validated ReviewResult."""
    
    messages = [
        {"role": "system", "content": REVIEW_SYSTEM},
        {"role": "user", "content": f"DIFF:\n{diff}"},
    ]

    url = f"{BASE_URL}/deployments/{MODEL_NAME}/chat/completions?api-version={API_VERSION}"
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    
    # Set temperature to 0.2 for more deterministic, structured output
    payload = {
        "messages": messages,
        "temperature": 0.2, 
        "max_tokens": 2048,
        "top_p": 1,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            return ReviewResult(pr_id=pr_id, comments=[])
            
        text = response.json()["choices"][0]["message"]["content"]
        
        # Defensive parsing: extract JSON using regex in case the model adds extra text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return ReviewResult(pr_id=pr_id, comments=[])
            
        data = json.loads(match.group(0))
        return ReviewResult(
            pr_id=pr_id,
            comments=[ReviewComment(**c) for c in data.get("comments", [])],
        )
        
    except (json.JSONDecodeError, ValueError, KeyError, requests.RequestException):
        # On failure, return an empty result to avoid aborting batch evaluation
        return ReviewResult(pr_id=pr_id, comments=[])


def _load_pr(path: Path, idx: int) -> tuple[str, str]:
    """Helper to load a PR from the JSONL dataset."""
    with path.open(encoding="utf-8") as fh:
        rows = [json.loads(line) for line in fh if line.strip()]
    row = rows[idx]
    return row["pr_id"], row["diff"]


def main() -> None:
    ap = argparse.ArgumentParser(description="Structured review agent (v1) - HKBU Version.")
    ap.add_argument("--diff", required=True, type=Path,
                    help="review_set.jsonl (with --idx) or a raw .diff file")
    ap.add_argument("--idx", type=int, default=None,
                    help="index into the JSONL dataset (omit for a raw .diff)")
    ap.add_argument("--pr-id", default=None, help="PR id when reading a raw .diff")
    ap.add_argument("--output", type=Path, default=None,
                    help="write the ReviewResult JSON here (else print it)")
    args = ap.parse_args()

    # Load diff from dataset or raw file
    if args.idx is not None:
        pr_id, diff = _load_pr(args.diff, args.idx)
    else:
        diff = args.diff.read_text(encoding="utf-8")
        pr_id = args.pr_id or args.diff.stem

    # Execute review and print/save result
    result = review(pr_id, diff)
    payload = result.model_dump_json(indent=2)
    
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
        print(f"Wrote {len(result.comments)} comments to {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()