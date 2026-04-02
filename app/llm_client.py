from openai import OpenAI

from app.config import Settings


class LLMClient:
    """Thin wrapper around the OpenAI client."""

    def __init__(self, settings: Settings) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model

    def get_chat_completion(self, user_message: str) -> str:
        """
        Send a user message to the model and return the text response.

        Args:
            user_message: The user's question or instruction.

        Returns:
            The assistant's response as a string.
        """
        response = self._client.responses.create(
            model=self._model,
            input=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant.",
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        return response.output_text.strip()