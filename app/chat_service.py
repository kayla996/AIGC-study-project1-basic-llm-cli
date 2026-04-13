from app.protocols import LLMClientProtocol
from app.logger import get_logger

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
        self.history = []

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

        logger.info(f"User question: {question}")
        answer = self._llm_client.get_chat_completion(cleaned_question)
        logger.info(f"Model answer: {answer}")
        self.history.append({"role":"user", "content": question})
        logger.info(f"current history: {self.history}")
        return answer