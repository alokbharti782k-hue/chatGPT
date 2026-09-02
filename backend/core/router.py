from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RouteDecision:
    route: str


def route_message(message: str) -> RouteDecision:
    """Minimal deterministic router; richer intent routing will be added later."""
    normalized = message.strip().lower()
    if not normalized:
        return RouteDecision(route="invalid")
    return RouteDecision(route="chat")
