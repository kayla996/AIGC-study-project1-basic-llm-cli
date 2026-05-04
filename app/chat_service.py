from app.protocols import LLMClientProtocol, RAGCoreProtocol
from app.logger import get_logger
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from app.config import get_settings
from app.rag.schemas import RetrievedChunk
from app.prompts import RAG_USER_PROMPT_TEMPLATE

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
    7. call model
    """

    def __init__(self, llm_client: LLMClientProtocol, prompt: str, max_history_count: int = 6, rag_core: RAGCoreProtocol | None = None) -> None:
        self._llm_client = llm_client
        self.history : list[ChatCompletionMessageParam] = []
        self.prompt = prompt
        self.max_history_count = max_history_count
        self._rag_core = rag_core
        self._settings = get_settings()


    def ask(self, question: str) -> str:
        """
        Validate input and get a response from the LLM client.

        Args:
            question: The user's question.

        Returns:
            The model's answer.
        """
        cleaned_question = question.strip()

        '''
        schema does the basic validation: like the question string cannot be void
        but it cannot detect if the user enter a space
        and we can add other rules here, like:
            string is overlong
            chat status illegal
            prompt config is wrong
            return value is void
        '''
        if not cleaned_question:
            logger.error(f"question validation failed: Question cannot be empty.")
            raise ValueError("Question cannot be empty.")

        logger.info(f"User question: {cleaned_question}")

        user_message: ChatCompletionMessageParam = {
            "role": "user",
            "content": cleaned_question,
        }
        self.history.append(user_message)
        # For saving token, only send 6 rounds of chat history
        self._trim_history()
        build_out_history = self._build_history()
        answer = self._llm_client.get_chat_completion(build_out_history)
        logger.info(f"Answer generated successfully: {answer}")
        assistant_message: ChatCompletionMessageParam = {
            "role": "assistant", "content": answer
        }
        self.history.append(assistant_message)
        self._trim_history()
        logger.info(f"current history: {self.history}")
        
        return answer
    
    def ask_with_rag(self, question: str, top_k: int | None = None):
        cleaned_question = question.strip()

        if not cleaned_question:
            logger.error(f"question validation failed: Question cannot be empty.")
            raise ValueError("Question cannot be empty.")
        
        logger.info(f"User question: {cleaned_question}")
        
        if self._rag_core is None:
            logger.error("Runtime Error: RAG core is not initialized.")
            raise RuntimeError("RAG core is not initialized.")
        
        retrieval_result = self._rag_core.retrieve_return_chunks(cleaned_question, top_k or self._settings.retrieval_top_k)
        rag_context = self._build_rag_context(retrieval_result.chunks)

        user_message: ChatCompletionMessageParam = {
            "role": "user",
            "content": RAG_USER_PROMPT_TEMPLATE.format(
                question=cleaned_question,
                context=rag_context
            )
        }
        self.history.append(user_message)
        self._trim_history()
        build_out_history = self._build_history()
        answer = self._llm_client.get_chat_completion(build_out_history)
        logger.info(f"Answer generated successfully: {answer}")
        assistant_message: ChatCompletionMessageParam = {
            "role": "assistant", "content": answer
        }
        self.history.append(assistant_message)
        self._trim_history()
        logger.info(f"current history: {self.history}")

        return answer, retrieval_result.chunks


    def _trim_history(self) -> None:
        if len(self.history) > self.max_history_count:
            self.history = self.history[-self.max_history_count: ]

    def _build_history(self) -> list[ChatCompletionMessageParam]:
        system_message: ChatCompletionMessageParam = {
            "role": "system",
            "content": self.prompt
        }
        return [system_message, *self.history]
    
    def clear_history(self) -> None:
        self.history.clear()
        logger.info("Conversation history cleared.")

    def _build_rag_context(self, retrieval_chunks: list[RetrievedChunk]) -> str:
        context_parts = []

        for index, chunk in enumerate(retrieval_chunks, start=1):
            context_parts.append(
                f"""[Source {index}]
source_id: {chunk.source_id}
chunk_id: {chunk.chunk_id}
score: {chunk.score:.4f}
context: {chunk.text}"""
            )

        return "\n\n".join(context_parts)