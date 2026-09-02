import json
import sqlite3
from pathlib import Path
from typing import Iterable

from backend.rag.chunker import Chunk
from backend.rag.loader import load_document


class RAGIndex:
    """Persistent SQLite lexical RAG index for local text/Markdown documents."""

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
        terms = {term.lower() for term in query.split() if term.strip()}
        if not terms:
            return []
        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute("SELECT source, text FROM chunks").fetchall()
        scored: list[tuple[str, str, float]] = []
        for source, text in rows:
            words = set(text.lower().split())
            score = len(terms & words) / len(terms)
            if score > 0:
                scored.append((source, text, score))
        scored.sort(key=lambda item: item[2], reverse=True)
        return scored[:top_k]
