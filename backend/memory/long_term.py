from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    key: str
    value: str


class LongTermMemory:
    """Provider-neutral long-term memory interface with an in-memory implementation."""

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}

    def put(self, key: str, value: str) -> None:
        self._records[key] = MemoryRecord(key=key, value=value)

    def get(self, key: str) -> MemoryRecord | None:
        return self._records.get(key)
