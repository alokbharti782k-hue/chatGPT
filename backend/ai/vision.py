from typing import Protocol


class VisionProvider(Protocol):
    async def analyze(self, image: bytes, prompt: str) -> str:
        ...


class NullVisionProvider:
    async def analyze(self, image: bytes, prompt: str) -> str:
        if not image:
            raise ValueError("Image payload cannot be empty")
        if not prompt.strip():
            raise ValueError("Vision prompt cannot be empty")
        raise NotImplementedError("Configure a vision provider")
