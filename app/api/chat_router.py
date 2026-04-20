from fastapi import APIRouter, HTTPException, Request, status

from app.api.schemas import ChatRequest, ChatResponse
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

