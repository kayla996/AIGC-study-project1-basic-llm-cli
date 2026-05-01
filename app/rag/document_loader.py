from __future__ import annotations

from pypdf import PdfReader
from pathlib import Path
from app.rag.schemas import SourceDocument


'''Responsible for loading the original file/files as the uniform SourceDocument object'''
class DocumentLoader:

    SUPPORT_EXTENSIONS = {".txt", ".pdf"}

    def load_file(self, file_path: str | Path) -> SourceDocument:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = path.suffix.lower()
        if suffix not in self.SUPPORT_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {suffix}"
                f"Supported types: {sorted(self.SUPPORT_EXTENSIONS)}"
            )
        
        if suffix == ".txt":
            print("load txt text...")
            return self.__load_text(path)

        if suffix == ".pdf":
            return self.__load_pdf(path)

        raise ValueError(f"Unsupported file type: {suffix}")

    def load_directory(self, dir_path: str | Path) -> list[SourceDocument]:
        path = Path(dir_path)

        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")

        documents: list[SourceDocument] = []
        print(f"Loading dic:{dir_path}")

        for file_path in sorted(path.iterdir()):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORT_EXTENSIONS:
                documents.append(self.load_file(file_path))

        return documents

    def __load_text(self, file_path: Path) -> SourceDocument:
        text = file_path.read_text(encoding="utf-8").strip()

        return SourceDocument(
            source_id=file_path.name,
            source_path=str(file_path),
            text=text,
            metadata={
                "file_type": "txt",
            }
        )
    
    def __load_pdf(self, file_path: Path) -> SourceDocument:
        reader = PdfReader(str(file_path))

        page_texts: list[str] = []
        for page_index, page in enumerate(reader.pages):
            extracted = (page.extract_text() or "").strip()
            if extracted:
                page_texts.append(extracted)

        # add \n\n in the end of each element in the list
        full_text = "\n\n".join((page_texts)).strip()

        return SourceDocument(
            source_id=file_path.name,
            source_path=str(file_path),
            text=full_text,
            metadata={
                "file_type": "pdf",
                "page_count": len(reader.pages)
            }
        )
        
