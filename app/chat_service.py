from app.protocols import LLMClientProtocol



class ChatService:
    """
    Business-level service for chat interactions.
    1. prompt assamble
    2. save chat history
    3. token count
    4. budget management
    5. safe check(validation)
    """

    def __init__(self, llm_client: LLMClientProtocol) -> None:
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