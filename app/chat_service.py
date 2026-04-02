from app.llm_client import LLMClient


class ChatService:
    """Business-level service for chat interactions."""

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm_client = llm_client

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
            raise ValueError("Question cannot be empty.")

        return self._llm_client.get_chat_completion(cleaned_question)