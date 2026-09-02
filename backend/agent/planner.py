from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Plan:
    goal: str
    steps: tuple[str, ...]


def create_plan(goal: str) -> Plan:
    goal = goal.strip()
    if not goal:
        raise ValueError("Agent goal cannot be empty")
    return Plan(goal=goal, steps=("understand", "execute", "verify"))
