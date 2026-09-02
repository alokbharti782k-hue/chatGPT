from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ThreatAssessment:
    blocked: bool
    severity: str
    reasons: tuple[str, ...]


_PATTERNS: tuple[tuple[str, str, str], ...] = (
    # Match common variants such as "ignore all previous instructions".
    ("prompt_injection", "high", r"ignore(?:\s+\w+){1,5}\s+instructions"),
    ("credential_exfiltration", "critical", r"(?:api[_ -]?key|password|secret|token).{0,40}(?:dump|exfiltrat|send|leak)"),
    ("shell_execution", "high", r"(?:rm\s+-rf|curl\s+[^\n]+\|\s*(?:sh|bash)|powershell\s+-enc)"),
    ("path_traversal", "high", r"(?:\.\./){2,}"),
    ("script_execution", "medium", r"<script\b|javascript:\s*"),
)


def assess_text(text: str) -> ThreatAssessment:
    if not text or len(text) > 20_000:
        return ThreatAssessment(True, "high", ("invalid_or_oversized_input",))

    normalized = " ".join(text.lower().split())
    reasons: list[str] = []
    highest = "low"
    rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    for name, severity, pattern in _PATTERNS:
        if re.search(pattern, normalized, flags=re.IGNORECASE | re.DOTALL):
            reasons.append(name)
            if rank[severity] > rank[highest]:
                highest = severity

    return ThreatAssessment(bool(reasons), highest, tuple(reasons))


def assess_many(values: Iterable[str]) -> ThreatAssessment:
    assessments = [assess_text(value) for value in values]
    reasons = tuple(reason for item in assessments for reason in item.reasons)
    severity = max((item.severity for item in assessments), key=lambda x: {"low": 0, "medium": 1, "high": 2, "critical": 3}[x], default="low")
    return ThreatAssessment(bool(reasons), severity, reasons)
