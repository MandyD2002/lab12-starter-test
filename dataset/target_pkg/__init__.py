"""target_pkg -- a tiny utility library used as the doc agent's target.

Four modules, twelve public functions total. The doc agent generates one
Markdown file per module; verify.py checks all twelve names are documented.
"""

from .collutil import chunk, group_by, unique
from .numutil import clamp, compute_average, percentage
from .textutil import slugify, truncate, word_count
from .validate import is_email, is_in_range, non_empty

__all__ = [
    "chunk", "group_by", "unique",
    "clamp", "compute_average", "percentage",
    "slugify", "truncate", "word_count",
    "is_email", "is_in_range", "non_empty",
]
