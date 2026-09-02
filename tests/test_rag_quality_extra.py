from backend.rag.text import tokenize


def test_tokenize_handles_underscores_and_numbers():
    assert tokenize("MSS_v2 sensor 2026") == ["mss_v2", "sensor", "2026"]
