from pathlib import Path

from backend.rag.index import RAGIndex


def test_rag_index_round_trip(tmp_path: Path):
    document = tmp_path / "notes.md"
    document.write_text("underground mining safety system", encoding="utf-8")
    index = RAGIndex(str(tmp_path / "rag.db"))

    assert index.index_document(document) == 1
    results = index.retrieve("mining safety", top_k=3)

    assert results
    assert results[0][0] == str(document.resolve())
    assert results[0][2] == 1.0
