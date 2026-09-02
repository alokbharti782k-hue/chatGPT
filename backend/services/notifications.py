from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Notification:
    title: str
    message: str
    severity: str = "info"


class NotificationService:
    """Provider-neutral notification boundary with no external side effects by default."""

    async def send(self, notification: Notification) -> None:
        if not notification.title.strip() or not notification.message.strip():
            raise ValueError("Notification title and message are required")
        raise NotImplementedError("Configure a notification provider")
