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
