import asyncio

from backend.agent.bounded import AgentLimits, BoundedAgentExecutor, build_tool_call
from backend.safety.permissions import PermissionPolicy
from backend.tools.registry import ToolRegistry
from backend.tools.runtime import ToolCall, ToolRuntime


def test_runtime_executes_only_allowlisted_tools():
    registry = ToolRegistry()
    registry.register("calculator", "safe arithmetic", lambda expression: expression)
    runtime = ToolRuntime(registry, allowed_tools=frozenset({"calculator"}))

    result = asyncio.run(runtime.execute([ToolCall("calculator", {"expression": "2+2"})]))
    assert result[0].success is True
    assert result[0].output == "2+2"


def test_runtime_rejects_non_allowlisted_tool():
    registry = ToolRegistry()
    registry.register("calculator", "safe arithmetic", lambda expression: expression)
    runtime = ToolRuntime(registry, allowed_tools=frozenset())

    result = asyncio.run(runtime.execute([ToolCall("calculator", {"expression": "2+2"})]))
    assert result[0].success is False
    assert "allowlisted" in (result[0].error or "")


def test_runtime_stops_after_first_tool_failure():
    registry = ToolRegistry()
    registry.register("first", "fails", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    registry.register("second", "should not run", lambda: "ok")
    runtime = ToolRuntime(registry, allowed_tools=frozenset({"first", "second"}))

    results = asyncio.run(runtime.execute([ToolCall("first", {}), ToolCall("second", {})]))
    assert len(results) == 1
    assert results[0].success is False


def test_bounded_agent_enforces_step_budget():
    registry = ToolRegistry()
    registry.register("echo", "echo", lambda value: value)
    runtime = ToolRuntime(registry, allowed_tools=frozenset({"echo"}))
    executor = BoundedAgentExecutor(runtime, AgentLimits(max_steps=1, max_tool_calls=5))

    result = asyncio.run(executor.run([
        [build_tool_call("echo", {"value": "one"})],
        [build_tool_call("echo", {"value": "two"})],
    ]))
    assert result.completed is False
    assert result.stop_reason == "max_steps_exceeded"


def test_iot_tools_remain_disabled_by_default():
    registry = ToolRegistry()
    registry.register("iot_write", "side effect", lambda: "changed")
    runtime = ToolRuntime(
        registry,
        allowed_tools=frozenset({"iot_write"}),
        permission_policy=PermissionPolicy(),
    )

    result = asyncio.run(runtime.execute([ToolCall("iot_write", {})]))
    assert result[0].success is False
    assert "disabled" in (result[0].error or "")
