from fastapi import APIRouter

from ai_director_backend.models import ChatRequest, ChatResponse, HealthResponse
from ai_director_backend.services.chat_service import build_chat_response


router = APIRouter(prefix="/api")


@router.get("/health", response_model=HealthResponse, tags=["system"])
async def health_check() -> HealthResponse:
    return HealthResponse()


@router.post("/chat", response_model=ChatResponse, tags=["chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    return await build_chat_response(request)
