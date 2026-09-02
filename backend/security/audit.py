from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from backend.security.redaction import redact_secrets


class SecurityAuditLog:
    """Append-only JSONL security audit log with basic secret redaction."""

    def __init__(self, path: str = "data/logs/security.jsonl") -> None:
        self.path = Path(path)

    def record(self, event: str, **details: object) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        safe = {key: redact_secrets(str(value)) for key, value in details.items()}
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            **safe,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
