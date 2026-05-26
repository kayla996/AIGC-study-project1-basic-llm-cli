from app.config import get_settings
from app.chat_service import ChatService
from app.llm_client import LLMClient
from app.rag.rag_core import RAGCore
from app.logger import get_logger

logger = get_logger(__name__)

'''
Test build/load index, retrieve chunks result based on the question and send to the llm to get the answer. 
And restrict the answer based on the retrieval chunks
'''
def main() -> None:
    settings = get_settings()
    llm_client = LLMClient(settings)
    rag_core = RAGCore(settings)
    chat_service = ChatService(llm_client, settings.rag_system_prompt, rag_core=rag_core)
    

    rag_core.build_or_load_default_index()

    while True:
        question = input("Question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            logger.info("User ends the conversation.")
            break

        try:
            response, tool_calls_output, source_chunks = chat_service.ask_with_tools(question, 3)

            print(f"\nQuestion: {question}")
            print(f"Retrieved {len(source_chunks)} chunk(s):\n")
            print(f"answer: {response}\n")
            print(f"tool calls output: {tool_calls_output}")

            for i, chunk in enumerate(source_chunks, start=1):
                print(f"[{i}] source={chunk.source_id} score={chunk.score:.4f}")
                print(chunk.text)
                print("-" * 80)

        except Exception as exc:
            logger.error(f"Retrieval failed: {exc}\n")
            print(f"Retrieval failed: {exc}\n")


if __name__ == "__main__":
    main()