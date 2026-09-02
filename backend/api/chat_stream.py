from __future__ import annotations

import json
from collections.abc import AsyncIterator
from uuid import uuid4

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.api.schemas import ChatRequest
from backend.core.orchestrator import Orchestrator

router = APIRouter(prefix="/api", tags=["chat"])
orchestrator = Orchestrator()


def _sse(event: str, payload: object) -> str:
    return f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    # Generate the conversation id before headers are sent so the client always
    # receives a stable id even when the provider is not configured.
    conversation_id = request.conversation_id or str(uuid4())
    # Preflight through the same orchestrator security boundary. The stream
    # performs the same checks again immediately before generation.
    orchestrator._prepare(request.message, conversation_id)

    async def events() -> AsyncIterator[str]:
        yield _sse("conversation", {"conversation_id": conversation_id})
        try:
            async for chunk in orchestrator.stream(request.message, conversation_id):
                yield _sse("delta", {"text": chunk})
        except Exception:
            # Do not expose provider internals, credentials, prompts, or stack traces.
            yield _sse("error", {"detail": "Streaming generation failed"})
            return
        yield _sse("done", {"conversation_id": conversation_id})

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )
