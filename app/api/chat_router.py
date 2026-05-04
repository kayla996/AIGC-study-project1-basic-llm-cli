from fastapi import APIRouter, HTTPException, Request, status

from app.api.schemas import ChatRequest, ChatResponse, RAGChatRequest, RAGChatResponse, SourceChunkItem
from app.chat_service import ChatService
from app.logger import get_logger

router = APIRouter(tags=["chat"])
logger = get_logger(__name__)


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    chat_service: ChatService = request.app.state.chat_service

    logger.info("POST /chat called.")

    try:
        answer = chat_service.ask(payload.question)
        return ChatResponse(answer=answer)
    except ValueError as exc:
        logger.warning("Bad request in /chat: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Unhandled error in /chat: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc

@router.post("/rag/chat", response_model=RAGChatResponse, status_code=status.HTTP_200_OK)
def rag_chat(payload: RAGChatRequest, request: Request) -> RAGChatResponse:
    chat_service : ChatService = request.app.state.chat_service

    logger.info("POST /rag/chat called.")

    try:
        answer, chunks = chat_service.ask_with_rag(payload.question, payload.top_k)
        response_chunks = [SourceChunkItem(
            source_id=chunk.source_id, 
            chunk_id=chunk.chunk_id,
            score=chunk.score,
            text=chunk.text
            ) 
            for chunk in chunks]
        return RAGChatResponse(answer=answer, source=response_chunks)
    except ValueError as exc:
        logger.warning("Bad request in /rag/chat: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Unhandled error in /rag/chat: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc
