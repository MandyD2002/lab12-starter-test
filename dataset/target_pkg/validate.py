"""Lightweight validators returning booleans (no exceptions on bad input)."""

import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_email(value: str) -> bool:
    """Return True if value looks like a single, well-formed email address."""
    return bool(_EMAIL_RE.match(value.strip()))


def is_in_range(value: float, low: float, high: float) -> bool:
    """Return True if low <= value <= high."""
    return low <= value <= high


def non_empty(value: str) -> bool:
    """Return True if value contains at least one non-whitespace character."""
    return bool(value and value.strip())
