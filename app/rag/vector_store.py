from __future__ import annotations

from pathlib import Path
import pickle

import numpy as np

from app.rag.schemas import DocumentChunk, RetrievedChunk
from app.config import get_settings
from app.logger import get_logger

logger = get_logger(__name__)
class VectorStore:

    def __init__(self) -> None:
        self._chunks: list[DocumentChunk] = []
        self._embeddings: np.ndarray | None = None
        self._settings = get_settings()

    '''
    Vectorize and permanent store chunks and embeddings (1 : 1), which are the indexes for further searching
    '''
    def add_chunks(
            self,
            chunks: list[DocumentChunk],
            embeddings: list[list[float]],
    ) -> None:
        if not chunks:
            return
        
        if len(chunks) != len(embeddings):
            raise ValueError(f"The number of chunks({len(chunks)}) and embeddings({len(embeddings)}) must match")

        new_embeddings = np.array(embeddings, dtype=np.float32)

        if self._embeddings is None:
            self._embeddings = new_embeddings
        else:
            self._embeddings = np.vstack([self._embeddings, new_embeddings])

        self._chunks.extend(chunks)

    '''
    According to the query embedding, search for the top k relevant chunks
    '''
    def search(
            self,
            query_embedding: list[float],
            top_k: int = 3,
    ) -> list[RetrievedChunk]:
        # Avoid searching chunks before setting up the indexes
        if self.is_empty():
            logger.warning("Vector store is empty. Need to call rag_core.build_or_load_default_index first")
            raise ValueError("Vector store is empty. Please build or load an index first")

        if top_k <= 0:
            logger.warning(f"top_k({top_k}) must be greater than 0.")
            raise ValueError(f"top_k({top_k}) must be greater than 0.")

        query_vector = np.array(query_embedding, dtype=np.float32)
        embeddings = self._embeddings 
        assert embeddings is not None

        scores = self._cosine_similarity(query_vector=query_vector, matrix=embeddings)
        top_k = min(top_k, len(self._chunks))

        top_indexes = np.argsort(scores)[::-1][:top_k]

        results: list[RetrievedChunk] = []
        for index in top_indexes:
            chunk = self._chunks[int(index)]
            score = float(scores[int(index)])

            # fillet the irrelevant chunks
            if score < self._settings.rag_retrieval_min_score:
                continue

            results.append(
                RetrievedChunk(
                    chunk_id=chunk.chunk_id,
                    source_id=chunk.source_id,
                    text=chunk.text,
                    score=score,
                    metadata=chunk.metadata
                )
            )

        return results
    
    def  save(self, persist_path: str | Path) -> None:
        path = Path(persist_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "chunks": self._chunks,
            "embeddings" : self._embeddings
        }

        with path.open("wb") as f:
            pickle.dump(payload, f)

    def load(self, persist_path: str | Path) -> None:
        print("run loading process...")
        path = Path(persist_path)
        if not path.exists():
            raise FileNotFoundError(f"Index file not found: {path}")

        with path.open("rb") as f:
            payload = pickle.load(f)

        self._chunks = payload["chunks"]
        self._embeddings = payload["embeddings"]

    def is_empty(self) -> bool:
        return len(self._chunks) == 0 or self._embeddings is None



    @staticmethod
    def _cosine_similarity(query_vector: np.ndarray, matrix: np.ndarray) -> np.ndarray:
        query_norm = np.linalg.norm(query_vector)
        matrix_norm = np.linalg.norm(matrix, axis=1)

        if query_norm == 0:
            raise ValueError("query embedding norm is zero")
        if np.any(matrix_norm == 0):
            raise ValueError("One or more stored embeddings have zero norm")
        
        return np.dot(matrix, query_vector) / (matrix_norm * query_norm)