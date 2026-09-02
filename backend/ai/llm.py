from typing import Protocol


class LLMProvider(Protocol):
    async def generate(self, message: str) -> str:
        ...


class LLMNotConfiguredError(RuntimeError):
    """Raised when an LLM provider has not been configured yet."""


class PlaceholderLLM:
    async def generate(self, message: str) -> str:
        raise LLMNotConfiguredError(
            "No LLM provider is configured. Set up a provider before calling the AI engine."
        )
