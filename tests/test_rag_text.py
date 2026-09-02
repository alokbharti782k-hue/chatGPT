from backend.rag.text import tokenize


def test_tokenize_normalizes_case_and_punctuation():
    assert tokenize("Miner-Safety, System!") == ["miner", "safety", "system"]
