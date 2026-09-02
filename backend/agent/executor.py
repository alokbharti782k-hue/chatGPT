from dataclasses import dataclass
from typing import Callable

from backend.agent.planner import Plan


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    completed: bool
    outputs: tuple[str, ...]


class AgentExecutor:
    """Constrained executor: callers explicitly provide allowed step handlers."""

    def execute(self, plan: Plan, handlers: dict[str, Callable[[], str]]) -> ExecutionResult:
        outputs: list[str] = []
        for step in plan.steps:
            handler = handlers.get(step)
            if handler is None:
                return ExecutionResult(False, tuple(outputs))
            outputs.append(handler())
        return ExecutionResult(True, tuple(outputs))
