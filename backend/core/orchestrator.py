from dataclasses import dataclass


@dataclass(slots=True)
class OrchestratorResult:
    response: str
    conversation_id: str


class Orchestrator:
    """Application coordinator; model/tool integrations will plug in here."""

    async def handle(self, message: str, conversation_id: str | None = None) -> OrchestratorResult:
        conversation_id = conversation_id or "default"
        return OrchestratorResult(
            response=f"ALICE received: {message}",
            conversation_id=conversation_id,
        )
