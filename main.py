from app.chat_service import ChatService
from app.config import get_settings
from app.llm_client import LLMClient
from app.fake_llm_client import FakeClient


def main() -> None:
    """CLI entry point."""
    try:
        settings = get_settings()
        # llm_client = LLMClient(settings)
        fake_Client = FakeClient()
        chat_service = ChatService(fake_Client)

        print("Simple LLM CLI is running.")
        print("Type your question and press Enter.")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            try:
                answer = chat_service.ask(user_input)
                print(f"AI: {answer}\n")
            except ValueError as exc:
                print(f"Input error: {exc}\n")
            except Exception as exc:
                print(f"Unexpected error: {exc}\n")

    except Exception as exc:
        print(f"Failed to start application: {exc}")


if __name__ == "__main__":
    main()