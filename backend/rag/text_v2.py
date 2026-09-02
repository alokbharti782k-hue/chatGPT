from __future__ import annotations

import re

_WORD_RE = re.compile(r"[A-Za-z0-9_]+")


def tokenize(text: str) -> list[str]:
    """Normalize text into deterministic alphanumeric tokens."""
    return [match.group(0).lower() for match in _WORD_RE.finditer(text)]
