from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.tools.runtime import ToolCall, ToolResult, ToolRuntime


@dataclass(frozen=True, slots=True)
class AgentLimits:
    max_steps: int = 5
    max_tool_calls: int = 5


@dataclass(frozen=True, slots=True)
class AgentRunResult:
    completed: bool
    steps: int
    results: tuple[ToolResult, ...]
    stop_reason: str | None = None


class BoundedAgentExecutor:
    """Runs model-produced tool plans under deterministic execution limits."""

    def __init__(self, runtime: ToolRuntime, limits: AgentLimits | None = None) -> None:
        self.runtime = runtime
        self.limits = limits or AgentLimits()
        if self.limits.max_steps < 1 or self.limits.max_tool_calls < 1:
            raise ValueError("Agent limits must be positive")

    async def run(self, plan: list[list[ToolCall]]) -> AgentRunResult:
        if len(plan) > self.limits.max_steps:
            return AgentRunResult(False, 0, (), "max_steps_exceeded")

        all_results: list[ToolResult] = []
        calls_used = 0
        for step_index, calls in enumerate(plan, start=1):
            if calls_used + len(calls) > self.limits.max_tool_calls:
                return AgentRunResult(False, step_index - 1, tuple(all_results), "max_tool_calls_exceeded")
            if not calls:
                return AgentRunResult(False, step_index - 1, tuple(all_results), "empty_step")

            results = await self.runtime.execute(calls)
            all_results.extend(results)
            calls_used += len(calls)
            if any(not result.success for result in results):
                return AgentRunResult(False, step_index, tuple(all_results), "tool_failure")

        return AgentRunResult(True, len(plan), tuple(all_results))


def build_tool_call(name: str, arguments: dict[str, Any]) -> ToolCall:
    """Small validation boundary for converting structured agent output to a call."""
    if not name.strip():
        raise ValueError("Tool name cannot be empty")
    if not isinstance(arguments, dict):
        raise TypeError("Tool arguments must be an object")
    return ToolCall(name=name, arguments=arguments)
