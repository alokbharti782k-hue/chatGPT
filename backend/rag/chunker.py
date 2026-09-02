from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Chunk:
    text: str
    index: int


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[Chunk]:
    if chunk_size <= 0 or overlap < 0:
        raise ValueError("Require chunk_size > 0 and overlap >= 0")
    if overlap >= chunk_size:
        overlap = max(0, chunk_size // 2)
    text = text.strip()
    if not text:
        return []

    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(Chunk(text=text[start:end], index=index))
        if end == len(text):
            break
        start = end - overlap
        index += 1
    return chunks
