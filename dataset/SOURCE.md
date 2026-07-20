# Review dataset — source and provenance

## What ships in this starter

This starter contains a **20-PR sample** of the labelled review set
(`review_set.jsonl`), enough to run the walkthrough end-to-end and to understand
the schema.

- **In-lab :** 5 PRs.
- **Held-out self-study :** 15 PRs.

## Schema

Each line of `review_set.jsonl` is one PR:

```json
{
  "pr_id": "string",
  "diff": "unified git diff as a string",
  "gold_comments": [
    {"line": 16, "severity": "major", "category": "bug", "description": "..."}
  ],
  "language": "Python"
}
```

- `severity` ∈ `{blocker, major, minor}`
- `category` ∈ `{bug, style, suggestion, nit}`
- `line` is the line number in the **new** file (the scoring matcher allows ±1).
