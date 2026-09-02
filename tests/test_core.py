from backend.rag.chunker import chunk_text
from backend.rag.retriever import KeywordRetriever
from backend.tools.calculator import calculate


def test_calculator_is_correct():
    assert calculate("2 + 3 * 4") == 14


def test_calculator_rejects_code():
    try:
        calculate("__import__('os').system('echo unsafe')")
    except ValueError:
        pass
    else:
        raise AssertionError("unsafe expression was accepted")


def test_chunker_overlap():
    chunks = chunk_text("abcdefghij", chunk_size=6, overlap=2)
    assert [c.text for c in chunks] == ["abcdef", "efghij"]


def test_keyword_retriever():
    chunks = chunk_text("mining safety system", chunk_size=100)
    results = KeywordRetriever().retrieve("mining safety", chunks)
    assert results and results[0].score == 1.0
