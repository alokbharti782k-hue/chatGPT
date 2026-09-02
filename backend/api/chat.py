from fastapi import APIRouter

from backend.api.schemas import ChatRequest, ChatResponse
from backend.core.orchestrator import Orchestrator

router = APIRouter(prefix="/api", tags=["chat"])
orchestrator = Orchestrator()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    result = await orchestrator.handle(request.message, request.conversation_id)
    return ChatResponse(response=result.response, conversation_id=result.conversation_id)
