import json
from pathlib import Path

from backend.rag.index import RAGIndex


FIXTURES = Path(__file__).with_name("rag_eval_cases.json")


def test_rag_evaluation_fixture_is_well_formed():
    cases = json.loads(FIXTURES.read_text(encoding="utf-8"))
    assert cases
    for case in cases:
        assert case["id"]
        assert case["query"]
        assert case["relevant"]


def test_retrieval_has_a_relevant_hit_for_representative_queries(tmp_path):
    index = RAGIndex(str(tmp_path / "rag.db"))
    docs = {
        "safety.md": "Underground mine safety depends on reliable monitoring and alerts.",
        "sensor.md": "An IoT gas sensor can detect methane, smoke, and other hazards.",
        "iot.md": "IoT based safety systems connect sensors to a monitoring gateway.",
        "gas.md": "The MQ 2 gas sensor is commonly used for smoke and combustible gas detection.",
    }
    for name, text in docs.items():
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        index.index_document(path)

    cases = json.loads(FIXTURES.read_text(encoding="utf-8"))
    for case in cases:
        results = index.retrieve(case["query"], top_k=3)
        assert results
        assert any(case["relevant"] in text.lower() for _, text, _ in results)
