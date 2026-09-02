import pytest

from backend.safety.permissions import PermissionDenied, PermissionPolicy, check_tool_permission
from backend.tools.calculator import calculate
from backend.tools.registry import ToolRegistry


def test_tool_registry_registers_and_resolves():
    registry = ToolRegistry()
    registry.register("calculator", "Basic arithmetic", calculate)
    assert registry.get("calculator").handler("2 + 2") == 4


def test_iot_permission_is_denied_by_default():
    with pytest.raises(PermissionDenied):
        check_tool_permission("iot_alarm", PermissionPolicy())


def test_external_permission_can_be_enabled():
    check_tool_permission("external_search", PermissionPolicy(allow_external_tools=True))
