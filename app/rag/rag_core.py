from __future__ import annotations

from pathlib import Path

from app.config import Settings
from app.rag.document_loader import DocumentLoader
from app.rag.embedder import Embedder
from app.rag.retriever import Retriever
from app.rag.schemas import RetrievalResult
from app.rag.text_splitter import TextSplitter
from app.rag.vector_store import VectorStore

class RAGCore:
    '''
    Week 3: build index + retrieve relevant text
    '''

    def __init__(
        self,
        settings: Settings,
        loader: DocumentLoader | None = None,
        splitter: TextSplitter | None = None,
        embedder: Embedder | None = None,
        vector_store: VectorStore | None = None,
        retriever: Retriever | None = None,
    ) -> None:
        self._settings = settings
        self._loader = loader or DocumentLoader()
        self._splitter = splitter or TextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        self._embedder = embedder or Embedder(settings)
        self._vector_store = vector_store or VectorStore()
        self._retriever = retriever or Retriever(self._embedder, self._vector_store)

        self._index_path = Path(settings.rag_index_dir) / "rag_index.pkl"


    def build_index_from_file(self, file_path: str) -> int:
        document = self._loader.load_file(file_path)
        chunks = self._splitter.split_document(document)

        if not chunks:
            return 0
        
        embeddings = self._embedder.embed_texts([chunk.text for chunk in chunks])
        self._vector_store.add_chunks(chunks, embeddings)
        self._vector_store.save(self._index_path)

        return len(chunks)

    def build_index_from_directory(self, dir_path: str) -> int:
        documents = self._loader.load_directory(dir_path)
        chunks = self._splitter.split_documents(documents)

        if not chunks: 
            return 0
        
        embeddings = self._embedder.embed_texts([chunk.text for chunk in chunks])
        self._vector_store.add_chunks(chunks, embeddings)
        self._vector_store.save(self._index_path)

        return len(chunks)
    
    def retrieve(self, question: str, top_k: int | None = None) -> RetrievalResult:
        effective_top_k = top_k or self._settings.retrieval_top_k
        return self._retriever.retrieve(question, effective_top_k)
    


    def build_or_load_default_index(self) -> None:
        """
        only for debug:
        - if there is local index, load it
        - or build from default data folder
        """
        if self._index_path.exists() and self._index_path.is_file():
            self._vector_store.load(self._index_path)
            return
        
        chunk_count = self.build_index_from_directory(
            self._settings.rag_data_dir
        )

        if chunk_count == 0:
            raise ValueError(
                f"No chunks were created from directory: {self._settings.rag_data_dir}. "
                "Please add supported .txt or .pdf files to the data folder."
            )