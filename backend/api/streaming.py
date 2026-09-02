from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator


async def stream_text(text: str, *, chunk_size: int = 64) -> AsyncIterator[str]:
    """Yield bounded text chunks while allowing cancellation between chunks."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")
    for start in range(0, len(text), chunk_size):
        await asyncio.sleep(0)
        yield text[start : start + chunk_size]
