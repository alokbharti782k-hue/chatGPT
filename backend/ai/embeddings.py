from typing import Protocol


class EmbeddingProvider(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class NullEmbeddingProvider:
    """Explicit fallback until a vector embedding provider is configured."""

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        raise RuntimeError("No embedding provider is configured")
