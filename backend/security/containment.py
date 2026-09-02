from __future__ import annotations

from dataclasses import dataclass

from backend.security.threat_detection import ThreatAssessment


@dataclass(frozen=True, slots=True)
class ContainmentDecision:
    allow: bool
    require_review: bool
    action: str


def decide(assessment: ThreatAssessment) -> ContainmentDecision:
    if not assessment.blocked:
        return ContainmentDecision(True, False, "allow")
    if assessment.severity == "critical":
        return ContainmentDecision(False, True, "isolate_and_review")
    if assessment.severity == "high":
        return ContainmentDecision(False, True, "block_and_review")
    return ContainmentDecision(False, False, "block")
