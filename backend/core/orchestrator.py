from collections.abc import AsyncIterator
from dataclasses import dataclass
from uuid import uuid4

from backend.ai.llm import LLMNotConfiguredError, build_llm
from backend.config.settings import get_settings
from backend.core.prompts import SYSTEM_PROMPT
from backend.core.router import route_message
from backend.memory.database import ConversationStore
from backend.safety.validator import validate_user_message
from backend.security.containment import decide
from backend.security.threat_detection import assess_text


@dataclass(slots=True)
class OrchestratorResult:
    response: str
    conversation_id: str


class Orchestrator:
    """Coordinates validation, defensive security gating, memory, routing, and the LLM."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.llm = build_llm(self.settings)
        self.store = ConversationStore(self.settings.database_path)

    def _prepare(self, message: str, conversation_id: str | None) -> tuple[str, list[tuple[str, str]]]:
        validation = validate_user_message(message)
        if not validation.allowed:
            raise ValueError(validation.reason or "Invalid message")

        security = assess_text(message)
        containment = decide(security)
        if not containment.allow:
            raise ValueError(
                f"Request blocked by ALICE security controls: {containment.action}"
            )

        if route_message(message).route == "invalid":
            raise ValueError("Invalid message")

        conversation_id = conversation_id or str(uuid4())
        history = self.store.get_messages(
            conversation_id, limit=self.settings.max_conversation_messages
        )
        return conversation_id, history

    async def handle(self, message: str, conversation_id: str | None = None) -> OrchestratorResult:
        conversation_id, history = self._prepare(message, conversation_id)
        self.store.add_message(conversation_id, "user", message)

        prompt = self._build_prompt(history, message)
        try:
            response = await self.llm.generate(prompt, SYSTEM_PROMPT)
        except LLMNotConfiguredError:
            response = (
                "ALICE is not connected to an LLM yet. Configure OPENAI_API_KEY in the environment "
                "to enable live AI responses."
            )

        self.store.add_message(conversation_id, "assistant", response)
        return OrchestratorResult(response=response, conversation_id=conversation_id)

    async def stream(self, message: str, conversation_id: str | None = None) -> AsyncIterator[str]:
        """Stream a response while persisting only a successfully completed turn."""
        conversation_id, history = self._prepare(message, conversation_id)
        self.store.add_message(conversation_id, "user", message)
        prompt = self._build_prompt(history, message)
        chunks: list[str] = []
        try:
            async for chunk in self.llm.stream(prompt, SYSTEM_PROMPT):
                chunks.append(chunk)
                yield chunk
        except LLMNotConfiguredError:
            fallback = (
                "ALICE is not connected to an LLM yet. Configure OPENAI_API_KEY in the environment "
                "to enable live AI responses."
            )
            chunks.append(fallback)
            yield fallback
            return

        response = "".join(chunks)
        self.store.add_message(conversation_id, "assistant", response)

    @staticmethod
    def _build_prompt(history: list[tuple[str, str]], message: str) -> str:
        if not history:
            return message
        lines = ["Conversation history:"]
        for role, content in history:
            lines.append(f"{role.upper()}: {content}")
        lines.extend(["", "CURRENT USER MESSAGE:", message])
        return "\n".join(lines)
