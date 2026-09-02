import asyncio

import pytest

from backend.api.streaming import stream_text


def test_stream_text_preserves_content() -> None:
    async def run() -> list[str]:
        return [chunk async for chunk in stream_text("hello world", chunk_size=4)]

    chunks = asyncio.run(run())
    assert "".join(chunks) == "hello world"
    assert all(1 <= len(chunk) <= 4 for chunk in chunks)


def test_stream_text_rejects_invalid_chunk_size() -> None:
    async def run() -> None:
        async for _ in stream_text("hello", chunk_size=0):
            pass

    with pytest.raises(ValueError):
        asyncio.run(run())


def test_stream_text_is_cancellable() -> None:
    async def run() -> None:
        iterator = stream_text("x" * 1000, chunk_size=1)
        task = asyncio.create_task(iterator.__anext__())
        await task
        await iterator.aclose()

    asyncio.run(run())
