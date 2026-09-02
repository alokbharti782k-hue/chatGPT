from collections.abc import AsyncIterator

from openai import AsyncOpenAI


class OpenAIProvider:
    """OpenAI-backed async LLM provider behind ALICE's provider interface."""

    def __init__(self, api_key: str, model: str, timeout_seconds: float = 30.0) -> None:
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key, timeout=timeout_seconds)

    async def generate(self, message: str, system_prompt: str | None = None) -> str:
        response = await self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=message,
        )
        return response.output_text

    async def _stream(self, message: str, system_prompt: str | None = None) -> AsyncIterator[str]:
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

    def stream(self, message: str, system_prompt: str | None = None) -> AsyncIterator[str]:
        return self._stream(message, system_prompt)
