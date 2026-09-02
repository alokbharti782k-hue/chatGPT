from pathlib import Path

import pytest

from backend.rag.loader import load_document


def test_load_supported_text_document(tmp_path: Path):
    path = tmp_path / "notes.md"
    path.write_text("Mining safety notes", encoding="utf-8")
    chunks = load_document(path)
    assert chunks and chunks[0].text == "Mining safety notes"


def test_reject_unsupported_document(tmp_path: Path):
    path = tmp_path / "notes.pdf"
    path.write_bytes(b"pdf")
    with pytest.raises(ValueError):
        load_document(path)
