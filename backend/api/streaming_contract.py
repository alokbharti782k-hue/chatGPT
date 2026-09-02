"""Provider-neutral contract for future native LLM streaming."""

from collections.abc import AsyncIterator
from typing import Protocol


class StreamingLLM(Protocol):
    async def stream(self, message: str, system_prompt: str) -> AsyncIterator[str]:
        """Yield text fragments without exposing provider-specific types."""
