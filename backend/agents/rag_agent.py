from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings


CHROMA_PATH = "chroma_db"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(

    persist_directory=CHROMA_PATH,
    embedding_function=embedding_model

)

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)


def rag_agent(state):

    question = state["question"]

    docs = retriever.invoke(
        question
    )

    context = "\n\n".join(

        [doc.page_content for doc in docs]

    )

    return {

        "context": context,
        "tool_context": state.get(
            "tool_context",
            ""
        ),
        "question": state["question"],
        "route": state["route"],
        "email": state["email"],
        "name": state["name"]

    }