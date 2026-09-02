from backend.rag.index import RAGIndex


def test_retrieval_handles_punctuation_and_prefers_phrase(tmp_path):
    database = tmp_path / "rag.db"
    first = tmp_path / "first.md"
    second = tmp_path / "second.md"
    first.write_text("Miner safety system uses gas sensors and deterministic alarms.", encoding="utf-8")
    second.write_text("General mining uses sensors.", encoding="utf-8")

    index = RAGIndex(str(database))
    index.index_documents([first, second])
    results = index.retrieve("miner safety system", top_k=2)

    assert results
    assert results[0][0] == str(first.resolve())
    assert results[0][2] > results[1][2]


def test_empty_query_returns_no_results(tmp_path):
    index = RAGIndex(str(tmp_path / "rag.db"))
    assert index.retrieve("   ") == []
