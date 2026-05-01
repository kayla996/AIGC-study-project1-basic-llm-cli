from __future__ import annotations

from openai import OpenAI

from app.config import Settings

class Embedder:
    # Embedding: Numeric vector
    # Responsible for embedding of text and query 

    def __init__(self, settings: Settings) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._module = settings.embedding_model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        # if judgment statement is to exclude the string like "\n", "\t", "\r", " "
        cleaned_texts = [text.strip() for text in texts if text and text.strip()]
        if not cleaned_texts:
            return []
        
        response = self._client.embeddings.create(
            model=self._module,
            input=cleaned_texts
        )

        return [item.embedding for item in response.data]
    
    def embed_query(self, query: str) -> list[float]:
        # if judgment statement is to exclude the string like "\n", "\t", "\r", " "
        cleaned_texts = query.strip()
        if not cleaned_texts:
            raise ValueError("Query cannot be empty")

        response = self._client.embeddings.create(
            model=self._module,
            input=cleaned_texts
        )

        return response.data[0].embedding
