"""Run a review-agent variant over a range of PRs and emit precision/recall.

Loads the named agent module (v1, v3, ...), runs its `review()` over each PR in
the range, scores against the gold labels with scoring.py, prints per-PR and
average precision/recall, and appends a row per PR to review_eval.csv. Tag each
run with --phase ("before", "after", "v1", "v3", ...) so the autograder can find
your final/tuned row.

Usage:
    python evaluate.py --agent v1 --pr-range 0:5 --phase before
    python evaluate.py --agent v3 --pr-range 0:5 --phase after
"""

import argparse
import csv
import importlib
import json
from pathlib import Path

from scoring import match_score, precision_recall

DEFAULT_DATASET = Path(__file__).parent / "dataset" / "review_set.jsonl"
DEFAULT_CSV = Path(__file__).parent / "review_eval.csv"


def load_prs(path: Path) -> list[dict]:
    with path.open() as fh:
        return [json.loads(line) for line in fh if line.strip()]


def parse_range(spec: str, n: int) -> range:
    """Parse a "start:end" slice spec (end exclusive); clamps to [0, n)."""
    start_s, _, end_s = spec.partition(":")
    start = int(start_s) if start_s else 0
    end = int(end_s) if end_s else n
    return range(max(0, start), min(end, n))


def main() -> None:
    ap = argparse.ArgumentParser(description="Score a review agent against gold labels.")
    ap.add_argument("--agent", default="v1", help="agent module name in review_agent/ (e.g. v1, v3)")
    ap.add_argument("--pr-range", default="0:5", help="start:end slice into the dataset")
    ap.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--phase", default="run", help="tag for this run (before/after/v1/v3/...)")
    args = ap.parse_args()

    agent = importlib.import_module(f"review_agent.{args.agent}")
    prs = load_prs(args.dataset)
    indices = parse_range(args.pr_range, len(prs))

    new_file = not args.csv.exists()
    with args.csv.open("a", newline="") as fh:
        writer = csv.writer(fh)
        if new_file:
            writer.writerow(["phase", "agent", "pr_id", "tp", "fp", "fn", "precision", "recall"])

        sum_p = sum_r = 0.0
        for i in indices:
            pr = prs[i]
            result = agent.review(pr["pr_id"], pr["diff"])
            tp, fp, fn = match_score(result.comments, pr["gold_comments"])
            prec, rec = precision_recall(tp, fp, fn)
            sum_p += prec
            sum_r += rec
            print(f"PR {i} ({pr['pr_id']}): precision={prec:.2f} recall={rec:.2f}  "
                  f"(TP={tp} FP={fp} FN={fn})")
            writer.writerow([args.phase, args.agent, pr["pr_id"], tp, fp, fn,
                             f"{prec:.4f}", f"{rec:.4f}"])

        k = len(indices) or 1
        avg_p, avg_r = sum_p / k, sum_r / k
        print(f"Average:  precision={avg_p:.2f}  recall={avg_r:.2f}")
        writer.writerow([f"{args.phase}-avg", args.agent, "AVERAGE", "", "", "",
                         f"{avg_p:.4f}", f"{avg_r:.4f}"])

    print(f"Appended results to {args.csv}")


if __name__ == "__main__":
    main()
