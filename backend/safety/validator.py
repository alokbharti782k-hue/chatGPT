from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationResult:
    allowed: bool
    reason: str | None = None


def validate_user_message(message: str) -> ValidationResult:
    text = message.strip()
    if not text:
        return ValidationResult(False, "Message cannot be empty")
    if len(text) > 10000:
        return ValidationResult(False, "Message exceeds the maximum length")
    return ValidationResult(True)
