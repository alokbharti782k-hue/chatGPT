from dataclasses import dataclass, field


@dataclass(slots=True)
class Message:
    role: str
    content: str


@dataclass
class ShortTermMemory:
    max_messages: int = 20
    messages: list[Message] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))
        if len(self.messages) > self.max_messages:
            del self.messages[:-self.max_messages]

    def get(self) -> list[Message]:
        return list(self.messages)
