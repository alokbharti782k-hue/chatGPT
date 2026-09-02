from collections.abc import AsyncIterator
from typing import Protocol

from backend.config.settings import Settings


class LLMProvider(Protocol):
    async def generate(self, message: str, system_prompt: str | None = None) -> str:
        ...

    def stream(self, message: str, system_prompt: str | None = None) -> AsyncIterator[str]:
        ...


class LLMNotConfiguredError(RuntimeError):
    """Raised when an LLM provider has not been configured yet."""


class PlaceholderLLM:
    async def generate(self, message: str, system_prompt: str | None = None) -> str:
        raise LLMNotConfiguredError(
            "No LLM provider is configured. Set OPENAI_API_KEY to enable ALICE's AI engine."
        )

    def stream(self, message: str, system_prompt: str | None = None) -> AsyncIterator[str]:
        async def _missing() -> AsyncIterator[str]:
            raise LLMNotConfiguredError(
                "No LLM provider is configured. Set OPENAI_API_KEY to enable ALICE's AI engine."
            )
            yield ""

        return _missing()


def build_llm(settings: Settings) -> LLMProvider:
    if not settings.openai_api_key:
        return PlaceholderLLM()

    from backend.ai.openai_provider import OpenAIProvider

    return OpenAIProvider(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        timeout_seconds=settings.llm_timeout_seconds,
    )
