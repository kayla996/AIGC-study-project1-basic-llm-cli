from app.chat_service import ChatService
from app.config import get_settings
from app.llm_client import LLMClient
from app.logger import get_logger


def main() -> None:
    """CLI entry point."""
    logger = get_logger(__name__)
    try:
        settings = get_settings()
        llm_client = LLMClient(settings)
        chat_service = ChatService(llm_client)

        print("Simple LLM CLI is running.")
        print("Type your question and press Enter.")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                logger.info(f"user exited the application")
                print("Goodbye!")
                break

            try:
                answer = chat_service.ask(user_input)
                print(f"AI: {answer}\n")
            except ValueError as exc:
                logger.warning(f"Input error: {exc}")
                print(f"Input error: {exc}\n")
            except Exception as exc:
                logger.exception(f"Unexpected error: {exc}")
                print(f"Unexpected error: {exc}\n")

    except Exception as exc:
        logger.exception(f"Failed to start application: {exc}")
        print(f"Failed to start application: {exc}")


if __name__ == "__main__":
    main()