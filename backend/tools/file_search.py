from pathlib import Path

from backend.rag.loader import load_document
from backend.rag.retriever import KeywordRetriever, RetrievedChunk


class LocalFileSearch:
    """Search supported local documents using the baseline RAG pipeline."""

    def __init__(self, documents_dir: str = "data/documents") -> None:
        self.documents_dir = Path(documents_dir)
        self.retriever = KeywordRetriever()

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        chunks = []
        for path in self.documents_dir.glob("*"):
            if path.suffix.lower() in {".txt", ".md"}:
                chunks.extend(load_document(path))
        return self.retriever.retrieve(query, chunks, top_k=top_k)
