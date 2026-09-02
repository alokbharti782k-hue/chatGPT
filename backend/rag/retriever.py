from dataclasses import dataclass

from backend.rag.chunker import Chunk


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    chunk: Chunk
    score: float


class KeywordRetriever:
    """Small dependency-free baseline retriever; vector retrieval can replace it later."""

    def retrieve(self, query: str, chunks: list[Chunk], top_k: int = 5) -> list[RetrievedChunk]:
        terms = {term.lower() for term in query.split() if term.strip()}
        if not terms:
            return []

        scored = []
        for chunk in chunks:
            words = set(chunk.text.lower().split())
            score = len(terms & words) / len(terms)
            if score > 0:
                scored.append(RetrievedChunk(chunk, score))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]
