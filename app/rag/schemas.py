from dataclasses import dataclass
from typing import Any

@dataclass
class SourceDocument:
    source_id: str              # 文件唯一标识，如文件名
    source_path: str            # 原始路径
    text: str                   # 文档原始全文
    metadata: dict[str, Any]

@dataclass
class DocumentChunk:
    """  
    Represent A file chunk split from the original file

    Attributes:
        chunk_id: The unique identifier for present text chuck
        source_id: The unique identifier of the original document, like filename
        text: The content of the current text chunk.
        chunk_index: The ordinal index of the current text chunk within the original document.
        metadata: Additional metadata, such as page number, title, paragraph position, and so on.
    """
    chunk_id: str
    source_id: str
    text: str
    chunk_index: int
    metadata: dict[str, Any]

@dataclass
class RetrievedChunk:
    """
    Represents a single text chunk returned by a retrieval operation.

    Attributes:
        chunk_id: The unique identifier of the retrieved text chunk.
        source_id: The unique identifier of the original document that contains the retrieved text chunk.
        text: The retrieved text content.
        score: The retrieval similarity score. In general, a higher score indicates greater relevance.
        metadata: Additional metadata, such as page number, title, original position, and so on.
    """
    chunk_id: str
    source_id: str
    text: str
    score: float
    metadata: dict[str, Any]


@dataclass
class RetrievalResult:
    """
    Represents the result of a complete retrieval operation.

    Attributes:
        question: The original question submitted by the user.
        chunks: The list of text chunks returned by the retrieval process.
    """
    question: str
    chunks: list[RetrievedChunk]
