from typing import Protocol
from openai.types.chat.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam


'''
abstract class: unique method different from Java
The subclass no need to inherit father class
Just use the same form of params and return value
… means it's an abstract class, can ignore the specific implement
'''
class LLMClientProtocol(Protocol):
    def get_chat_completion(self, messages: list[ChatCompletionAssistantMessageParam]) -> str:
        ...