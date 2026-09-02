from __future__ import annotations

import asyncio
import inspect
import time
from dataclasses import dataclass
from typing import Any

from backend.safety.permissions import PermissionDenied, PermissionPolicy, check_tool_permission
from backend.security.containment import decide
from backend.security.threat_detection import assess_text
from backend.tools.registry import ToolRegistry


@dataclass(frozen=True, slots=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ToolResult:
    name: str
    success: bool
    output: object | None = None
    error: str | None = None
    duration_ms: int = 0


class ToolRuntime:
    """Bounded, allowlisted tool execution boundary.

    The runtime validates tool names and text inputs/outputs, enforces a per-run
    call budget and timeout, and delegates permission decisions to the safety
    policy. It never evaluates arbitrary code or accepts a callable from the
    model itself.
    """

    def __init__(
        self,
        registry: ToolRegistry,
        *,
        allowed_tools: frozenset[str] | None = None,
        permission_policy: PermissionPolicy | None = None,
        max_calls: int = 5,
        timeout_seconds: float = 10.0,
    ) -> None:
        if max_calls < 1:
            raise ValueError("max_calls must be at least 1")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.registry = registry
        self.allowed_tools = allowed_tools
        self.permission_policy = permission_policy or PermissionPolicy()
        self.max_calls = max_calls
        self.timeout_seconds = timeout_seconds

    async def execute(self, calls: list[ToolCall]) -> list[ToolResult]:
        if len(calls) > self.max_calls:
            raise ValueError("Tool call budget exceeded")

        results: list[ToolResult] = []
        for call in calls:
            results.append(await self._execute_one(call))
            if not results[-1].success:
                break
        return results

    async def _execute_one(self, call: ToolCall) -> ToolResult:
        started = time.monotonic()
        try:
            if self.allowed_tools is not None and call.name not in self.allowed_tools:
                raise PermissionDenied(f"Tool is not allowlisted: {call.name}")
            check_tool_permission(call.name, self.permission_policy)

            tool = self.registry.get(call.name)
            if tool is None:
                raise ValueError(f"Unknown tool: {call.name}")

            argument_text = repr(call.arguments)
            assessment = assess_text(argument_text)
            if not decide(assessment).allow:
                raise PermissionDenied("Tool arguments blocked by security policy")

            result = tool.handler(**call.arguments)
            if inspect.isawaitable(result):
                result = await asyncio.wait_for(result, timeout=self.timeout_seconds)

            output_assessment = assess_text(str(result))
            if not decide(output_assessment).allow:
                raise PermissionDenied("Tool output blocked by security policy")

            return ToolResult(
                name=call.name,
                success=True,
                output=result,
                duration_ms=int((time.monotonic() - started) * 1000),
            )
        except Exception as exc:
            return ToolResult(
                name=call.name,
                success=False,
                error=str(exc),
                duration_ms=int((time.monotonic() - started) * 1000),
            )
