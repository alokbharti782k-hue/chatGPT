from __future__ import annotations


def validate_document_bytes(data: bytes) -> None:
    """Reject content that should never enter the document/RAG pipeline."""
    if b"\x00" in data:
        raise ValueError("Binary content is not accepted")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Document must be valid UTF-8 text") from exc
