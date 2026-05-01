from __future__ import annotations

from app.rag.schemas import RetrievalResult
from app.rag.embedder import Embedder
from app.rag.vector_store import VectorStore

class Retriever:
    '''question -> embedding -> top-k search'''

    def __init__(self, embedder: Embedder, vector_store: VectorStore) -> None:
        self._embedder = embedder
        self._vector_store = vector_store

    def retrieve(self, question: str, top_k: int = 3) -> RetrievalResult:
        clean_question = question.strip()
        if not clean_question:
            raise ValueError("Question cannot be empty")

        query_embedding = self._embedder.embed_query(clean_question)
        chunks = self._vector_store.search(query_embedding, top_k)

        return RetrievalResult(
            question=clean_question,
            chunks=chunks
        )