
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BACKEND_DIR = Path(__file__).resolve().parents[1]
CHROMA_DIR = BACKEND_DIR / "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
)


def get_retriever():
    """Open the existing database or fail with an actionable message."""

    if not CHROMA_DIR.is_dir():
        raise RuntimeError(
            f"Knowledge-base database not found at {CHROMA_DIR}. "
            "Run `python backend/ingest.py` from the project root first."
        )

    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_model,
    )

    if db._collection.count() == 0:
        raise RuntimeError(
            f"Knowledge-base database at {CHROMA_DIR} is empty. "
            "Rebuild it using the ingestion script."
        )

    return db.as_retriever(search_kwargs={"k": 3})


def rag_agent(state):
    retriever = get_retriever()

    question = state["question"]
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    return {
        "context": context,
        "tool_context": state.get("tool_context", ""),
        "question": question,
        "route": state["route"],
        "email": state["email"],
        "name": state["name"],
    }