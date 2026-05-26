import json

from openai.types.chat.chat_completion_tool_union_param import ChatCompletionToolUnionParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from app.protocols import LLMClientProtocol, RAGCoreProtocol
from app.logger import get_logger
from app.config import get_settings
from app.rag.schemas import RetrievedChunk
from app.prompts import RAG_USER_PROMPT_TEMPLATE
from app.tools.registry import get_tool_definitions
from app.tools.executor import ToolExecutor
from app.tools.schemas import ToolCallRecord, ToolExecutionResult

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

    def ask_with_tools(self, question: str, top_k: int | None = None):
        cleaned_question = question.strip()

        if not cleaned_question:
            logger.error(f"question validation failed: Question cannot be empty.")
            raise ValueError("Question cannot be empty.")
        
        logger.info(f"User question: {cleaned_question}")
        
        if self._rag_core is None:
            logger.error("Runtime Error: RAG core is not initialized.")
            raise RuntimeError("RAG core is not initialized.")
        
        user_message: ChatCompletionMessageParam = {
            "role": "user",
            "content": cleaned_question,
        }
        self.history.append(user_message)
        self._trim_history()
        first_messages = self._build_using_tools_history()
        tools = get_tool_definitions()

        logger.info(f"Fist tool call message: {first_messages}")

        first_response = self._llm_client.get_chat_completion_with_tools(
            messages=first_messages,
            tools=tools,
            tool_choice="auto")
        
        logger.info(f"Fist tool call response: {first_response}")

        if first_response is None:
            logger.error("First call returned None.")
            raise RuntimeError("First call returned None.")
        
        if not first_response.tool_calls:
            first_response_message : ChatCompletionMessageParam = {
                "role": "assistant",
                "content": first_response.content or ""
            }

            self.history.append(first_response_message)
            self._trim_history()
            return first_response.content or "", [], []
        

        tool_calls_output = []
        sources = []
            
        
        executor = ToolExecutor(self._rag_core)

        first_response_message : ChatCompletionMessageParam = {
                "role": "assistant",
                "content": first_response.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name, # type: ignore
                            "arguments": tool_call.function.arguments, # type: ignore
                        }
                    }
                    for tool_call in first_response.tool_calls
                ]
            }
        
        self.history.append(first_response_message)

        for tool_call in first_response.tool_calls:
            tool_name = tool_call.function.name # type: ignore
            tool_args = tool_call.function.arguments # type: ignore

            execution_result = executor.execute(tool_name, tool_args)

            tool_payload = ToolExecutionResult(
                tool_name=execution_result.tool_name,
                success=execution_result.success,
                result=execution_result.result,
                error=execution_result.error
            )

            tool_calls_output.append(
                ToolCallRecord(
                    name=tool_name,
                    argument= json.loads(tool_args or "{}"),
                    success=execution_result.success,
                    error=execution_result.error,
                    result=execution_result.result
                )
            )

            logger.info(f"Tool calls output: {tool_calls_output}")

            if tool_name == "search_knowledge_base" and execution_result.success:
                result_data = execution_result.result
                if isinstance(result_data, dict) and result_data is not None:
                    chunks = result_data.get("chunks", [])
                    sources.extend(chunks)
                else:
                    chunks = []

            self.history.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_payload.model_dump_json()
                }
            )
            self._trim_history()
            final_message = self._build_using_tools_history()

            logger.info(f"Final tool calls message: {final_message}")

            final_response = self._llm_client.get_chat_completion_with_tools(
                messages=final_message,
                tools=tools,
                tool_choice="none"
            )

            logger.info(f"Final tool calls response: {final_response}")

        return final_response.content or "", tool_calls_output, sources


    def _trim_history(self) -> None:
        if len(self.history) > self.max_history_count:
            self.history = self.history[-self.max_history_count: ]

    def _build_history(self) -> list[ChatCompletionMessageParam]:
        system_message: ChatCompletionMessageParam = {
            "role": "system",
            "content": self.prompt
        }
        return [system_message, *self.history]
    
    def _build_using_tools_history(self) -> list[ChatCompletionMessageParam]:
        system_message: ChatCompletionMessageParam = {
            "role": "system",
            "content": f"{self.prompt}, You are a tool-using AI assistant. Use tools when needed."
        }
        return [system_message, *self.history]
    
    def clear_history(self) -> None:
        self.history.clear()
        logger.info("Conversation history cleared.")

    def _build_rag_context(self, retrieval_chunks: list[RetrievedChunk]) -> str:
        context_parts = []

        for index, chunk in enumerate(retrieval_chunks, start=1):
            context_parts.append(
                f"""
[Source {index}]
source_id: {chunk.source_id}
chunk_id: {chunk.chunk_id}
score: {chunk.score:.4f}
context: {chunk.text}"""
            )

        return "\n\n".join(context_parts)