import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""
    openai_api_key: str
    openai_model: str


def get_settings() -> Settings:
    """
    Load and validate application settings.

    Raises:
        ValueError: If required environment variables are missing.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Please set it in your .env file."
        )

    return Settings(
        openai_api_key=api_key,
        openai_model=model,
    )