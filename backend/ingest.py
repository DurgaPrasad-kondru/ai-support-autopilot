
import os
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
DATA_DIR = PROJECT_DIR / "docs"
CHROMA_DIR = BACKEND_DIR / "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def create_vector_database():
    """Build the Chroma database from the project's TXT knowledge-base files."""

    if not DATA_DIR.is_dir():
        raise FileNotFoundError(f"Knowledge-base directory not found: {DATA_DIR}")

    text_files = sorted(DATA_DIR.glob("*.txt"))

    if not text_files:
        raise FileNotFoundError(f"No .txt knowledge-base files found in {DATA_DIR}")

    documents = []

    for file_path in text_files:
        print(f"Loading knowledge-base file: {file_path.name}")
        loader = TextLoader(str(file_path), encoding="utf-8")
        documents.extend(loader.load())

    if not documents:
        raise ValueError("The knowledge-base files contain no readable documents.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No text chunks were created from the knowledge base.")

    print(f"Creating embeddings for {len(chunks)} chunks...")

    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=str(CHROMA_DIR),
    )

    print(f"Ingestion completed. Database location: {CHROMA_DIR}")
    return str(CHROMA_DIR)


if __name__ == "__main__":
    create_vector_database()