from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SearchResult:
    title: str
    url: str
    snippet: str


class WebSearchTool:
    """Provider-neutral web search interface; no network access is enabled by default."""

    def __init__(self, provider=None) -> None:
        self.provider = provider

    async def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        if not query.strip():
            raise ValueError("Search query cannot be empty")
        if self.provider is None:
            return []
        return await self.provider.search(query, limit=limit)
