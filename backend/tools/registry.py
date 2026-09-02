from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Tool:
    name: str
    description: str
    handler: Callable[..., object]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, name: str, description: str, handler: Callable[..., object]) -> None:
        if not name.strip():
            raise ValueError("Tool name cannot be empty")
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")
        self._tools[name] = Tool(name, description, handler)

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list(self) -> list[Tool]:
        return list(self._tools.values())
