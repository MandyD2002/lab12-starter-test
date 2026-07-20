"""v0 -- the naive free-form code-review agent (HKBU GPT Version).

This is the deliberately-bad baseline you run first in the walkthrough. It just
asks the model to "review this diff" and prints whatever prose comes back.

Usage:
    python review_agent/v0.py --pr dataset/review_set.jsonl --idx 0
"""

import argparse
import json
import os
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

# HKBU GPT Gateway Configuration
# Fetches the key loaded from your local workspace file automatically
API_KEY = os.getenv("HKBU_API_KEY")
BASE_URL = "https://genai.hkbu.edu.hk/api/v0/rest"
MODEL_NAME = "gpt-4.1"
API_VERSION = "2024-12-01-preview"

NAIVE_PROMPT = "You are a senior engineer. Review this Git diff and tell me what you think."


def review_freeform(diff: str) -> str:
    """Ask the HKBU GPT model to review a diff and return the raw text response."""
    
    # Defensive execution check: prevent silent failure if the key was not resolved
    if not API_KEY:
        return "[ERROR]: HKBU_API_KEY missing! Please check if your .env file exists and contains the correct key."

    # Pack the prompt messages using the standard OpenAI payload format
    messages = [
        {"role": "system", "content": NAIVE_PROMPT},
        {"role": "user", "content": f"DIFF:\n{diff}"},
    ]

    # Assemble the specific deployment REST endpoint target
    url = f"{BASE_URL}/deployments/{MODEL_NAME}/chat/completions?api-version={API_VERSION}"
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    
    # Max tokens is elevated to 2048 to prevent truncated code analysis
    payload = {
        "messages": messages, 
        "temperature": 0.7, 
        "max_tokens": 2048, 
        "top_p": 1, 
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # Parse response payload and traverse down to extract the response string
            res_json = response.json()
            return res_json["choices"][0]["message"]["content"]
        else:
            return f"[ERROR {response.status_code}]: {response.text}"
            
    except Exception as e:
        return f"[CONNECTION ERROR]: {str(e)}"


def load_pr(path: Path, idx: int) -> dict:
    """Load the idx-th PR record from a JSONL dataset."""
    with path.open(encoding="utf-8") as fh:
        rows = [json.loads(line) for line in fh if line.strip()]
    return rows[idx]


def main() -> None:
    ap = argparse.ArgumentParser(description="Naive free-form review agent (v0) - HKBU Version.")
    ap.add_argument("--pr", required=True, type=Path, help="path to review_set.jsonl")
    ap.add_argument("--idx", type=int, default=0, help="0-based index of the PR to review")
    args = ap.parse_args()

    pr = load_pr(args.pr, args.idx)
    print(f"# Free-form review of {pr['pr_id']}\n")
    print(review_freeform(pr["diff"]))
    print(
        "\n--- Ask yourself: is this line-anchored? severity-tagged? "
        "free of nitpicks? postable as PR comments? ---"
    )


if __name__ == "__main__":
    main()