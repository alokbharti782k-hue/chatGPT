import asyncio

import pytest

from backend.api.streaming import stream_text


@pytest.mark.asyncio
async def test_stream_text_preserves_content() -> None:
    chunks = [chunk async for chunk in stream_text("hello world", chunk_size=4)]
    assert "".join(chunks) == "hello world"
    assert all(1 <= len(chunk) <= 4 for chunk in chunks)


@pytest.mark.asyncio
async def test_stream_text_rejects_invalid_chunk_size() -> None:
    with pytest.raises(ValueError):
        async for _ in stream_text("hello", chunk_size=0):
            pass


@pytest.mark.asyncio
async def test_stream_text_is_cancellable() -> None:
    iterator = stream_text("x" * 1000, chunk_size=1)
    task = asyncio.create_task(iterator.__anext__())
    await task
    await iterator.aclose()
