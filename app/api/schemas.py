from pydantic import BaseModel, Field
from typing import Any

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

class ToolChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")
    top_k: int | None = None
class ToolCallItem(BaseModel):
    name: str
    argument: dict[str, Any]
    success: bool
    result: Any | None = None
    error: str| None = None

class ToolChatResponse(BaseModel):
    answer: str
    tool_calls: list[ToolCallItem]
    sources: list[dict[str, Any]] = []
