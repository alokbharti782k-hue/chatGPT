import sqlite3
from pathlib import Path


class ConversationStore:
    """SQLite-backed conversation store with a small provider-neutral API."""

    def __init__(self, database_path: str = "data/database/alice.db") -> None:
        self.database_path = database_path
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS messages ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "conversation_id TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, "
                "created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
            )

    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, role, content),
            )

    def get_messages(self, conversation_id: str, limit: int = 20) -> list[tuple[str, str]]:
        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute(
                "SELECT role, content FROM messages WHERE conversation_id = "
                "? ORDER BY id DESC LIMIT ?",
                (conversation_id, limit),
            ).fetchall()
        return list(reversed(rows))
