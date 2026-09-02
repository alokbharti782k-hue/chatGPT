import json
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Iterable

from backend.rag.chunker import Chunk
from backend.rag.loader import load_document
from backend.rag.text import tokenize


class RAGIndex:
    """Persistent, dependency-free lexical RAG index for text/Markdown documents."""

    def __init__(self, database_path: str = "data/database/alice_rag.db") -> None:
        self.database_path = database_path
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(database_path) as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS chunks ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "source TEXT NOT NULL, chunk_index INTEGER NOT NULL, text TEXT NOT NULL, "
                "metadata TEXT NOT NULL DEFAULT '{}', "
                "UNIQUE(source, chunk_index))"
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_chunks_source ON chunks(source)")

    def index_document(self, path: str | Path) -> int:
        file_path = Path(path).resolve()
        chunks = load_document(file_path)
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("DELETE FROM chunks WHERE source = ?", (str(file_path),))
            connection.executemany(
                "INSERT INTO chunks (source, chunk_index, text, metadata) VALUES (?, ?, ?, ?)",
                [(str(file_path), c.index, c.text, json.dumps({"source": str(file_path)})) for c in chunks],
            )
        return len(chunks)

    def index_documents(self, paths: Iterable[str | Path]) -> int:
        return sum(self.index_document(path) for path in paths)

    def retrieve(self, query: str, top_k: int = 5) -> list[tuple[str, str, float]]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        query_counts = Counter(query_tokens)
        query_terms = set(query_tokens)
        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute("SELECT source, text FROM chunks").fetchall()

        scored: list[tuple[str, str, float]] = []
        for source, text in rows:
            document_tokens = tokenize(text)
            if not document_tokens:
                continue
            document_counts = Counter(document_tokens)
            matched = query_terms & document_counts.keys()

            if matched:
                coverage = len(matched) / len(query_terms)
                frequency = sum(min(document_counts[t], query_counts[t]) for t in matched)
                frequency_score = min(frequency / max(len(query_tokens), 1), 1.0)
                phrase_bonus = 0.25 if " ".join(query_tokens) in " ".join(document_tokens) else 0.0
                score = min(coverage * 0.65 + frequency_score * 0.35 + phrase_bonus, 1.0)
            else:
                # Preserve a deterministic zero-score fallback so callers can
                # distinguish "no lexical match" from an empty index.
                score = 0.0
            scored.append((source, text, score))

        scored.sort(key=lambda item: item[2], reverse=True)
        return scored[:top_k]
