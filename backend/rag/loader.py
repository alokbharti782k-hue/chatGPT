from pathlib import Path

from backend.rag.chunker import Chunk, chunk_text

SUPPORTED_EXTENSIONS = {".txt", ".md"}


def load_document(path: str | Path) -> list[Chunk]:
    file_path = Path(path)
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError("Only .txt and .md documents are supported by the baseline loader")
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    return chunk_text(file_path.read_text(encoding="utf-8"))
