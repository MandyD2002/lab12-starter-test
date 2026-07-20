# Lab 12 — Starter

AI-assisted code review and automated documentation. See the lab handout
(`lab-12-student.pdf`) for the full walkthrough. You build two agents — a
structured **review agent** you tune against labelled ground truth, and a
**doc agent** that generates API docs from a Python package — then wire both
into a GitHub Actions workflow that runs on every PR.

## Setup
**In Anaconda Prompt**
```bash
cd Desktop
git clone https://github.com/MandyD2002/lab12-starter-test.git
cd lab12-starter-test
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env_example .env
```
**Go to `.env` and input your HKBU GenAI API key**

## Files
- `review_agent/v0.py` — naive free-form reviewer (the bad baseline you run first).
- `review_agent/v1.py` — **SKELETON you implement and tune.** The Pydantic
  `ReviewComment`/`ReviewResult` schema and the parse plumbing are fixed; you
  change the prompt (and optionally add post-filtering) to raise precision.
- `scoring.py` — **provided.** TP/FP/FN matcher + precision/recall. Do not edit.
- `evaluate.py` — runs an agent variant over a PR range → prints metrics and
  appends to `review_eval.csv`.
- `doc_agent/agent.py` — **provided.** AST-then-feed doc generator (enumerates
  public names with the AST first so the model can't hallucinate them).
- `doc_agent/verify.py` — structural check that every public name is documented.
- `dataset/review_set.jsonl` — **20-PR sample** of the labelled set .
- `dataset/target_pkg/` — 4-file utility library (12 public functions) for the doc agent.

## Run
```bash
# 1. Feel the bad baseline (free-form prose, not postable):
python review_agent/v0.py --pr dataset/review_set.jsonl --idx 0

# 2. Score v1, then tune the prompt and re-score:
python evaluate.py --agent v1 --pr-range 0:5 --phase before
#    ... edit REVIEW_SYSTEM in review_agent/v1.py, log each revision in tuning_notes.md ...
python evaluate.py --agent v1 --pr-range 0:5 --phase v1.1

# 3. Generate docs:
python doc_agent/agent.py --pkg dataset/target_pkg/ --out generated_docs/
#   ... verify the generated docs:
python doc_agent/verify.py --pkg dataset/target_pkg/ --docs generated_docs/
#    Expected: PASS: 12 public names, 12 documented (100%)
```
Run all commands from this directory (`starter/lab-12/`) so the
`review_agent`/`doc_agent` package imports resolve.

## Before push back to the repository
**Run**
``` bash
git add .
git commit -m "fix: update review and doc agents for lab completion"
git checkout -b feature/my-agent-updates
git push origin feature/my-agent-updates
``` 

## Deliverables
- `review_agent/` — your tuned implementation.
- `doc_agent/` — the doc agent (provided; keep it working).
- `review_eval.csv` — precision/recall before **and** after tuning, all in-lab PRs.
- `generated_docs/` — doc output for `target_pkg`.
- `tuning_notes.md` — ≥ 3 prompt revisions, **honestly** reporting any recall lost.
- A test PR URL where the GitHub Action posted the agent's review automatically. (need to test this part)

## Notes
- The rubric targets **precision ≥ 0.7** with **recall ≥ 0.4** (the recall floor
  blocks a trivial "never comment" agent that games precision). In code review,
  false positives cost more than false negatives — accept lower recall for
  actionable precision, and say so in your notes.
- Pin your SDK versions in `requirements.txt`; an unpinned `pip install` can
  balloon the Action's install time.
- Never commit your API key.
