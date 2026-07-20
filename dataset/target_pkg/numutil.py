"""Numeric helpers: averages, clamping, and percentage maths."""

from collections.abc import Sequence

_DEFAULT_PRECISION = 2  # private: not part of the documented public surface


def compute_average(values: Sequence[float]) -> float:
    """Return the arithmetic mean of values, or 0.0 for an empty sequence."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def clamp(value: float, low: float, high: float) -> float:
    """Clamp value into the inclusive range [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(value, high))


def percentage(part: float, whole: float) -> float:
    """Return part as a percentage of whole, rounded to two decimal places.

    Returns 0.0 when whole is zero rather than raising.
    """
    if whole == 0:
        return 0.0
    return round(part / whole * 100, _DEFAULT_PRECISION)
