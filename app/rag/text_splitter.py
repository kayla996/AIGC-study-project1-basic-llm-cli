from __future__ import annotations

from pprint import pprint
from app.rag.schemas import SourceDocument, DocumentChunk
from app.config import get_settings

class TextSplitter:
    settings = get_settings()

    def __init__(self, chunk_size: int = settings.chunk_size, chunk_overlap: int = settings.chunk_overlap) -> None:
        if chunk_size <= 0:
            raise ValueError("Chunk size must greater than 0")

        if chunk_overlap < 0:
            raise ValueError("Chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError("Chunk_overlap must be smaller than chunk_size")
        
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap

    def split_document(self, document: SourceDocument) -> list[DocumentChunk]:
        text = self._normalize_text(document.text)
        if not text:
            return []
        
        raw_chunks = self._split_text(text)
        pprint(f"raw chunks = \n{raw_chunks}")
        chunks: list[DocumentChunk] = []
        for index, chunk_text in enumerate(raw_chunks):
            chunk = DocumentChunk(
                chunk_id=f"{document.source_id}_chunk_{index}",
                source_id=document.source_id,
                text=chunk_text,
                chunk_index=index,
                metadata={
                    **document.metadata,
                    "source_path": document.source_path
                }
            )
            chunks.append(chunk)
        
        return chunks

    def split_documents(self, documents: list[SourceDocument]) -> list[DocumentChunk]:
        all_chunks: list[DocumentChunk] = []

        for document in documents:
            all_chunks.extend(self.split_document(document))

        return all_chunks

    def _split_text(self, text: str) -> list[str]:
        chunks: list[str] = []
        start = 0
        windows_size = self._chunk_size - self._chunk_overlap

        while start < len(text):
            end = start + self._chunk_size
            chunk = text[start: end].strip()

            if chunk:
                chunks.append(chunk)

            start += windows_size
        return chunks

    @staticmethod
    def _normalize_text(text: str) -> str:
        # text clean: delete the space of text start and end, compress the space lines
        lines = [line.strip() for line in text.splitlines()]
        non_empty_lines = [line for line in lines if line]
        return "\n".join(non_empty_lines).strip()