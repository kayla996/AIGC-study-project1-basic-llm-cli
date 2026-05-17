from app.rag.rag_core import RAGCore
from app.tools.schemas import SourceChunkItem, KnowledgeBaseSearchResult, KnowledgeBaseSearchArgs 

def  search_knowledge_base(rag_core: RAGCore, question: str, top_k: int = 3) ->KnowledgeBaseSearchResult:
    args = KnowledgeBaseSearchArgs(question=question, top_k=top_k)

    # question = question.strip()

    if rag_core is None:
        raise ValueError("RAG Core is not available")

    rag_core.build_or_load_default_index()
    retrieval_result = rag_core.retrieve_return_chunks(question, top_k)

    chunks : list[SourceChunkItem] = []
    for chunk in retrieval_result.chunks:
        chunks.append(SourceChunkItem(
            source_id=chunk.source_id,
            chunk_id=chunk.chunk_id,
            score=chunk.score,
            text=chunk.text))
        
    return KnowledgeBaseSearchResult(
        question=args.question,
        top_k=args.top_k,
        chunks=chunks
        )