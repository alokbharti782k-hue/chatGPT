from collections.abc import AsyncIterator

from openai import APIError, AuthenticationError, RateLimitError
from openai import AsyncOpenAI


class LLMProviderError(RuntimeError):
    """Safe, user-facing wrapper for an upstream LLM API failure."""


class OpenAIProvider:
    """OpenAI-backed async LLM provider behind ALICE's provider interface."""

    def __init__(self, api_key: str, model: str, timeout_seconds: float = 30.0) -> None:
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key, timeout=timeout_seconds)

    @staticmethod
    def _translate_error(exc: APIError) -> LLMProviderError:
        if isinstance(exc, AuthenticationError):
            return LLMProviderError("OpenAI rejected the configured API key. Check OPENAI_API_KEY in Railway Variables.")
        if isinstance(exc, RateLimitError):
            return LLMProviderError("OpenAI rejected the request because the project is rate-limited or has no available quota.")
        return LLMProviderError(f"OpenAI API error while using the configured model: {exc.__class__.__name__}.")

    async def generate(self, message: str, system_prompt: str | None = None) -> str:
        try:
            response = await self.client.responses.create(
                model=self.model,
                instructions=system_prompt,
                input=message,
            )
        except APIError as exc:
            raise self._translate_error(exc) from exc
        return response.output_text

    async def _stream(self, message: str, system_prompt: str | None = None) -> AsyncIterator[str]:
        try:
            stream = await self.client.responses.create(
                model=self.model,
                instructions=system_prompt,
                input=message,
                stream=True,
            )
            async for event in stream:
                if getattr(event, "type", None) == "response.output_text.delta":
                    delta = getattr(event, "delta", "")
                    if delta:
                        yield delta
        except APIError as exc:
            raise self._translate_error(exc) from exc

    def stream(self, message: str, system_prompt: str | None = None) -> AsyncIterator[str]:
        return self._stream(message, system_prompt)
