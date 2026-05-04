from app.config import get_settings
from app.rag.rag_core import RAGCore

'''
Test build/load index, retrieve chunk result based on the question
'''
def main() -> None:
    settings = get_settings()
    rag_core = RAGCore(settings)

    try:
        rag_core.build_or_load_default_index()
    except Exception as exc:
        print(f"Failed to build or load index: {exc}")
        return

    print("RAG debug CLI is running.")
    print("Type your question and press Enter.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            result = rag_core.retrieve_return_chunks(question)

            print(f"\nQuestion: {result.question}")
            print(f"Retrieved {len(result.chunks)} chunk(s):\n")

            for i, chunk in enumerate(result.chunks, start=1):
                print(f"[{i}] source={chunk.source_id} score={chunk.score:.4f}")
                print(chunk.text)
                print("-" * 80)

        except Exception as exc:
            print(f"Retrieval failed: {exc}\n")


if __name__ == "__main__":
    main()