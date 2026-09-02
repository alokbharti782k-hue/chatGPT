from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SpeechResult:
    text: str


class SpeechService:
    """Provider-neutral speech boundary for future STT/TTS integrations."""

    async def transcribe(self, audio: bytes) -> SpeechResult:
        if not audio:
            raise ValueError("Audio payload cannot be empty")
        raise NotImplementedError("Configure a speech provider")

    async def synthesize(self, text: str) -> bytes:
        if not text.strip():
            raise ValueError("Text cannot be empty")
        raise NotImplementedError("Configure a speech provider")
