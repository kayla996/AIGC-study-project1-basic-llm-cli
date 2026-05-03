import os
from dataclasses import dataclass

from dotenv import load_dotenv

from app.prompts import DEFAULT_SYSTEM_PROMPT, RAG_SYSTEM_PROMPT


load_dotenv()

# LLM defaults
DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

# RAG defaults
DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 100
DEFAULT_RETRIEVAL_TOP_K = 3


# Path defaults
DEFAULT_RAG_DATA_DIR = "data/raw"
DEFAULT_RAG_INDEX_DIR = "data/index"

# server defaults
DEFAULT_APP_HOST = "127.0.0.1"
DEFAULT_APP_PORT = 8000

'''
1. Load the setting from .env by dotenv, saving in an inner class
2. Check if api key exist
'''

# @dataclass will automatically create a constructor faction with all params required
# "frozen=True" set config obj as unchangeable
@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""
    openai_api_key: str
    openai_model: str
    system_prompt: str
    app_host: str
    app_port: int

    # rag related
    embedding_model: str
    rag_data_dir: str
    rag_index_dir: str
    chunk_size: int
    chunk_overlap: int
    retrieval_top_k: int
    rag_system_prompt: str
    rag_retrieval_min_score: float = 0.45


'''
get_settings is not a class-level method
but it's used to create settings obj
why we don't turn it to constructor?
it's a design mode called factory mode
if it's constructor, 
    1.when we try to test, we can only rely on the real params from os. Otherwise, we can write down the fake params in constructor
    2.when we try to test, we cannot get the params from other way: JSON FILE, console, database, FastAPI etc. 
    3.a constructor should be responded to multiple purposes, like reading os params, validation, save data etc.
'''
def get_settings() -> Settings:
    """
    Load and validate application settings.

    Raises:
        ValueError: If required environment variables are missing.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    openai_model = os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL).strip()
    system_prompt = os.getenv("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)
    app_host = os.getenv("APP_HOST", DEFAULT_APP_HOST).strip()
    app_port = int(os.getenv("APP_PART", DEFAULT_APP_PORT))

    embedding_model = os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL).strip()
    rag_data_dir = os.getenv("RAG_DATA_DIR", DEFAULT_RAG_DATA_DIR).strip()
    rag_index_dir = os.getenv("RAG_INDEX_DIR", DEFAULT_RAG_INDEX_DIR).strip()

    chunk_size = int(os.getenv("CHUNK_SIZE", DEFAULT_CHUNK_SIZE))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", DEFAULT_CHUNK_OVERLAP))
    retrieval_top_k = int(os.getenv("RETRIEVAL_TOP_K", DEFAULT_RETRIEVAL_TOP_K))

    rag_system_prompt = os.getenv("RAG_SYSTEM_PROMPT", RAG_SYSTEM_PROMPT).strip()
    rag_retrieval_min_score = float(os.getenv("RETRIEVAL_MIN_SCORE", str(Settings.rag_retrieval_min_score)))

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Please set it in your .env file."
        )

    return Settings(
        openai_api_key=api_key,
        openai_model=openai_model,
        system_prompt=system_prompt,
        app_host=app_host,
        app_port=app_port,
        embedding_model=embedding_model,
        rag_data_dir=rag_data_dir,
        rag_index_dir=rag_index_dir,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        retrieval_top_k=retrieval_top_k,
        rag_system_prompt=rag_system_prompt,
        rag_retrieval_min_score=rag_retrieval_min_score
    )