from typing import Protocol

class LLMClientProtocol(Protocol):
    def get_chat_completion(self, question: str) -> str:
        ...