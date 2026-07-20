"""Match generated review comments to gold labels (PROVIDED -- do not edit).

This is the ground-truth matcher. evaluate.py calls it to turn a ReviewResult
plus a PR's gold_comments into precision/recall. Read it carefully: the matching
rule (line within +/-1, category must agree) is exactly what the rubric measures,
so understanding it tells you what your tuning is actually optimising.
"""

from review_agent.v1 import ReviewComment


def match_score(generated: list[ReviewComment],
                gold: list[dict]) -> tuple[int, int, int]:
    """Returns (true_positives, false_positives, false_negatives).

    A generated comment matches a gold comment if:
    - line numbers within +/-1 (diffs are noisy), AND
    - category matches.
    Each gold comment can be matched at most once; unmatched generated comments
    are false positives and unmatched gold comments are false negatives.
    """
    matched_gold_idx: set[int] = set()
    tp = 0
    fp = 0
    for gen in generated:
        match = None
        for i, g in enumerate(gold):
            if i in matched_gold_idx:
                continue
            if abs(gen.line - g["line"]) <= 1 and gen.category == g["category"]:
                match = i
                break
        if match is not None:
            matched_gold_idx.add(match)
            tp += 1
        else:
            fp += 1
    fn = len(gold) - len(matched_gold_idx)
    return tp, fp, fn


def precision_recall(tp: int, fp: int, fn: int) -> tuple[float, float]:
    """Precision and recall from a (tp, fp, fn) triple; 0.0 when undefined."""
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    return prec, rec
