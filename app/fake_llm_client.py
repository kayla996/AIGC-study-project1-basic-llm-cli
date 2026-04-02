class FakeClient:
    def get_chat_completion(self, question: str) -> str:
        return "fake client answering!"