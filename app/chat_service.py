from app.protocols import LLMClientProtocol
from app.logger import get_logger
from openai.types.chat.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam

logger = get_logger(__name__)

class ChatService:
    """
    Business-level service for chat interactions.
    1. Prompt assembly
    2. save chat history
    3. token count
    4. budget management
    5. safe check(validation)
    6. muti-round chat history append
    """

    def __init__(self, llm_client: LLMClientProtocol) -> None:
        self._llm_client = llm_client
        self.history : list[ChatCompletionAssistantMessageParam] = []

    def ask(self, question: str) -> str:
        """
        Validate input and get a response from the LLM client.

        Args:
            question: The user's question.

        Returns:
            The model's answer.
        """
        cleaned_question = question.strip()
        if not cleaned_question:
            logger.error(f"question validation failed: Question cannot be empty.")
            raise ValueError("Question cannot be empty.")

        logger.info(f"User question: {cleaned_question}")

        user_message: ChatCompletionAssistantMessageParam = {
            "role": "user",
            "content": cleaned_question,
        }
        self.history.append(user_message)
        # Saving token, only send 6 rounds of chat history
        recent_history = self.history[-6:]
        answer = self._llm_client.get_chat_completion(recent_history)
        logger.info(f"Model answer: {answer}")
        assistant_message: ChatCompletionAssistantMessageParam = {
            "role": "assistant", "content": answer
        }
        self.history.append(assistant_message)
        logger.info(f"current history: {self.history}")
        return answer