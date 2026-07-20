"""Small string helpers used across the example utility library."""

import re

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Convert text to a lowercase, hyphen-separated URL slug.

    Non-alphanumeric runs collapse to a single hyphen and leading/trailing
    hyphens are stripped.
    """
    return _SLUG_RE.sub("-", text.strip().lower()).strip("-")


def truncate(text: str, limit: int, suffix: str = "...") -> str:
    """Truncate text to at most limit characters, appending suffix if cut."""
    if limit < 0:
        raise ValueError("limit must be non-negative")
    if len(text) <= limit:
        return text
    keep = max(0, limit - len(suffix))
    return text[:keep] + suffix


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in text."""
    return len(text.split())


def _normalise(text: str) -> str:
    """Internal: collapse internal whitespace (private, not documented)."""
    return " ".join(text.split())
