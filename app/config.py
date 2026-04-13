import os
from dataclasses import dataclass

from dotenv import load_dotenv

from app.prompts import DEFAULT_SYSTEM_PROMPT


load_dotenv()

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

'''
get_settings is not a class-level method
but it's used to create settings obj
why we don't turn it to constructor?
it's a design mode called factory mode
if it's constructor, 
    1.when we try to test, we can only rely on the real params from os. Otherwise, we can write down the fake params in constructor
    2.when we try to test, we cannot get the params from other way: JSON FILE, console, database, FastAPI etc. 
    3.a constructor should be responsed to multiple purposes, like reading os params, validation, save data etc.
'''
def get_settings() -> Settings:
    """
    Load and validate application settings.

    Raises:
        ValueError: If required environment variables are missing.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
    system_prompt = os.getenv("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Please set it in your .env file."
        )

    return Settings(
        openai_api_key=api_key,
        openai_model=model,
        system_prompt=system_prompt
    )