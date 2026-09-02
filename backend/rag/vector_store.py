from dataclasses import dataclass

from backend.rag.chunker import Chunk


@dataclass(frozen=True, slots=True)
class IndexedChunk:
    chunk: Chunk
    document_id: str


class InMemoryVectorStore:
    """Provider-neutral index placeholder for a future embedding/vector database."""

    def __init__(self) -> None:
        self._items: list[IndexedChunk] = []

    def add(self, document_id: str, chunks: list[Chunk]) -> None:
        self._items.extend(IndexedChunk(chunk, document_id) for chunk in chunks)

    def all(self) -> list[IndexedChunk]:
        return list(self._items)
