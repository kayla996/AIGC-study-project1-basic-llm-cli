from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")

class ChatResponse(BaseModel):
    answer: str

class SourceChunkItem(BaseModel):
    source_id: str
    chunk_id: str
    score: float
    text: str

class RAGChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")
    top_k: int | None = None

class RAGChatResponse(BaseModel):
    answer: str
    source: list[SourceChunkItem]