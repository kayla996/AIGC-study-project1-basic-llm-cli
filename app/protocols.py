from typing import Protocol
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from app.rag.schemas import RetrievalResult


'''
abstract class: unique method different from Java
The subclass no need to inherit father class
Just use the same form of params and return value
… means it's an abstract class, can ignore the specific implement
'''
class LLMClientProtocol(Protocol):
    def get_chat_completion(self, messages: list[ChatCompletionMessageParam]) -> str:
        ...

    def get_chat_completion_with_tools(
            self, 
            messages: list[ChatCompletionMessageParam], 
            tools: list[ChatCompletionToolUnionParam]
    ):

class RAGCoreProtocol(Protocol):
    def retrieve_return_chunks(self, question: str, top_k: int | None = None) -> RetrievalResult:
        ...

    def build_or_load_default_index(self) -> None:
        ...