"""Collection helpers: chunking, de-duplication, and grouping."""

from collections.abc import Callable, Hashable, Iterable
from itertools import islice
from typing import TypeVar

_T = TypeVar("_T")
_K = TypeVar("_K", bound=Hashable)


def chunk(items: Iterable[_T], size: int) -> list[list[_T]]:
    """Split items into consecutive lists of at most size elements."""
    if size <= 0:
        raise ValueError("size must be positive")
    it = iter(items)
    out: list[list[_T]] = []
    while batch := list(islice(it, size)):
        out.append(batch)
    return out


def unique(items: Iterable[_T]) -> list[_T]:
    """Return items with duplicates removed, preserving first-seen order."""
    seen: set = set()
    out: list[_T] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def group_by(items: Iterable[_T], key: Callable[[_T], _K]) -> dict[_K, list[_T]]:
    """Group items into a dict keyed by key(item), preserving insertion order."""
    groups: dict[_K, list[_T]] = {}
    for item in items:
        groups.setdefault(key(item), []).append(item)
    return groups
