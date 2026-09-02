from pathlib import Path

from backend.memory.database import ConversationStore


def test_conversation_store_round_trip(tmp_path: Path):
    store = ConversationStore(str(tmp_path / "alice.db"))
    store.add_message("c1", "user", "hello")
    store.add_message("c1", "assistant", "hi")
    store.add_message("c2", "user", "other")

    assert store.get_messages("c1") == [("user", "hello"), ("assistant", "hi")]
    assert store.get_messages("c2") == [("user", "other")]


def test_conversation_store_limit(tmp_path: Path):
    store = ConversationStore(str(tmp_path / "alice.db"))
    for index in range(5):
        store.add_message("c1", "user", str(index))

    assert store.get_messages("c1", limit=2) == [("user", "3"), ("user", "4")]
