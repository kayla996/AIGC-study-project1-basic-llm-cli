from openai import OpenAI
from app.config import Settings
from app.logger import get_logger
from openai.types.chat.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam


'''call openai model'''

logger = get_logger(__name__)

class LLMClient:
    """Thin wrapper around the OpenAI client."""

    def __init__(self, settings: Settings) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model
        self.prompt = settings.system_prompt

    def get_chat_completion(self, messages: list[ChatCompletionAssistantMessageParam]) -> str:
        """
        Send a user message to the model and return the text response.

        Args:
            user_message: The user's question or instruction.

        Returns:
            The assistant's response as a string.
        """
        logger.info(f'question to model: {messages}')
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "developer", "content": self.prompt},
                *messages,
            ],
        )
        logger.info(f"------end connect to the model-------")
        return completion.choices[0].message.content or ""