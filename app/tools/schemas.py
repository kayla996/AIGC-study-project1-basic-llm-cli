from pydantic import BaseModel, Field
from typing import Any


class ToolExecutionResult(BaseModel):
    tool_name: str
    success: bool
    result: Any | None = None
    error: str | None = None
    raw: dict | None = None

class CalculatorArgs(BaseModel):
    expression: str = Field(
        min_length=1,
        description="A simple arithmetic expression, such as '12 * 3 + 34'"
    )

class KnowledgeBaseSearchArgs(BaseModel):
    question: str = Field(
        min_length=1,
        description="The search question for the local RAG knowledge base."
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of chunk of retrieve."
    )

class SourceChunkItem(BaseModel):
    source_id: str | None = None
    chunk_id: str
    score: float | None = None
    text: str

class KnowledgeBaseSearchResult(BaseModel):
    question: str
    top_k: int
    chunks: list[SourceChunkItem]

class ToolCallRecord(BaseModel):
    name: str
    argument: dict[str, Any]
    success: bool
    result: Any | None = None
    error: str | None = None