from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PermissionPolicy:
    allow_external_tools: bool = False
    allow_iot_actions: bool = False
    require_confirmation_for_side_effects: bool = True


class PermissionDenied(PermissionError):
    pass


def check_tool_permission(tool_name: str, policy: PermissionPolicy) -> None:
    if tool_name.startswith("iot_") and not policy.allow_iot_actions:
        raise PermissionDenied("IoT actions are disabled by policy")
    if tool_name.startswith("external_") and not policy.allow_external_tools:
        raise PermissionDenied("External tools are disabled by policy")
