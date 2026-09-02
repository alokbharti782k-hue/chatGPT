from dataclasses import dataclass
from uuid import uuid4

from backend.ai.llm import LLMNotConfiguredError, build_llm
from backend.config.settings import get_settings
from backend.core.prompts import SYSTEM_PROMPT
from backend.core.router import route_message
from backend.safety.validator import validate_user_message


@dataclass(slots=True)
class OrchestratorResult:
    response: str
    conversation_id: str


class Orchestrator:
    """Coordinates validation, routing, and the configured LLM provider."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.llm = build_llm(self.settings)

    async def handle(self, message: str, conversation_id: str | None = None) -> OrchestratorResult:
        validation = validate_user_message(message)
        if not validation.allowed:
            raise ValueError(validation.reason or "Invalid message")

        if route_message(message).route == "invalid":
            raise ValueError("Invalid message")

        conversation_id = conversation_id or str(uuid4())
        try:
            response = await self.llm.generate(message, SYSTEM_PROMPT)
        except LLMNotConfiguredError:
            response = (
                "ALICE is not connected to an LLM yet. Configure OPENAI_API_KEY in the environment "
                "to enable live AI responses."
            )
        return OrchestratorResult(response=response, conversation_id=conversation_id)
