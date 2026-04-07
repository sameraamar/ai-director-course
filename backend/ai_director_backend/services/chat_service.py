import logging

from ai_director_backend.models import ChatRequest, ChatResponse
from ai_director_backend.retrieval.engine import (
    build_grounded_response_from_chunks,
    build_out_of_scope_response,
    build_personal_question_response,
    build_scoped_ai_response,
    is_personal_question,
    retrieve_chunks,
)
from ai_director_backend.services.gemini_service import answer_with_scoped_gemini, can_call_gemini, synthesize_with_gemini

logger = logging.getLogger(__name__)


async def build_chat_response(request: ChatRequest) -> ChatResponse:
    if is_personal_question(request.question):
        logger.info("Chat request routed to personal-question out-of-scope response for question: %s", request.question)
        result = build_personal_question_response()
    else:
        chunks = retrieve_chunks(question=request.question, user_mode=request.user_mode)
        if not chunks:
            if can_call_gemini():
                scoped_answer = await answer_with_scoped_gemini(request.question)
                if scoped_answer:
                    logger.info("Chat request answered with scoped Gemini synthesis for question: %s", request.question)
                    result = build_scoped_ai_response(scoped_answer)
                else:
                    logger.info("Chat request routed to out-of-scope response after scoped Gemini check for question: %s", request.question)
                    result = build_out_of_scope_response()
            else:
                logger.info("Chat request routed to out-of-scope response for question: %s", request.question)
                result = build_out_of_scope_response()
        else:
            gemini_answer = await synthesize_with_gemini(question=request.question, chunks=chunks)
            if gemini_answer:
                logger.info("Chat request answered with Gemini synthesis for question: %s", request.question)
            else:
                logger.info("Chat request answered with local synthesis fallback for question: %s", request.question)
            result = build_grounded_response_from_chunks(question=request.question, chunks=chunks, answer=gemini_answer)

    return ChatResponse(
        question=request.question,
        answer=result["answer"],
        grounded=result["grounded"],
        status=result["status"],
        answer_source=result["answer_source"],
        citations=result["citations"],
    )
