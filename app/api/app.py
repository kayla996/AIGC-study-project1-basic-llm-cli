from fastapi import FastAPI

from app.api.chat_router import router as chat_router
from app.chat_service import ChatService
from app.config import get_settings
from app.llm_client import LLMClient
from app.rag.rag_core import RAGCore

'''
Create the whole app:
    similar to the main.py in CLI mode
    login all the method can be used 
'''
def create_app() -> FastAPI:
    settings = get_settings()
    llm_client = LLMClient(settings)
    rag_core = RAGCore(settings)
    rag_core.build_or_load_default_index()
    chat_service = ChatService(
        llm_client=llm_client, 
        prompt=settings.system_prompt,
        rag_core=rag_core
    )

    app = FastAPI(
        title="PROJECT1 API",
        version="0.1.0",
        description="Week 2: FASTAPI chat service"
    )

    app.state.chat_service = chat_service
    app.include_router(chat_router)

    # this interface worked on the whole app
    # so cannot be written in any router file
    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app

app = create_app()
