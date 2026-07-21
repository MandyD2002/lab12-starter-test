# Review-agent tuning notes (reference)

Operating point we are aiming for: **high precision, recall is allowed to drop.**
In code review a reviewer who cries wolf gets muted; one who surfaces ~half of
real bugs at high precision stays trusted. The cost-of-error asymmetry sets the
target, not F1. We **accept lower recall in exchange for actionable precision**
and report that honestly below.

All numbers are the average over the 5 in-lab PRs (`evaluate.py --pr-range 0:5`).

| Phase | Change | Precision | Recall | Verdict |
|-------|--------|-----------|--------|---------|
| v1    | baseline starter prompt | 0.53 | 0.57 | too many nitpicks |
| v1.1  | Add Search Strategy | 0.53 | 0.5 | precision held, recall down |
| v1.2  | Remove Search Strategy + add more rule | 0.60 | 0.50 | PR3 still tricky |
| v1.3  | Add instructions to ask the AI to follow | 0.73 | 0.60 | Final |


## Round-by-round

### v1 — first attempt (baseline)
Ran the starter prompt unchanged. (Write what you found in the results)

### v

## Honest recall statement

(Write you statement here)
