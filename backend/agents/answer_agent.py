import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(

    groq_api_key=os.getenv("GROQ_API_KEY"),

    model_name="openai/gpt-oss-20b"

)


def answer_agent(state):

    question = state["question"]

    context = state["context"]

    tool_context = state.get(
        "tool_context",
        ""
    )

    prompt = f"""

    You are an AI customer support assistant.

    Answer the customer professionally.

    Context:
    {context}

    Tool Context:
    {tool_context}

    Question:
    {question}

    """

    response = llm.invoke(
        prompt
    )

    return {

        "answer": response.content,
        "question": state["question"],
        "context": state["context"],
        "tool_context": tool_context,
        "route": state["route"],
        "email": state["email"],
        "name": state["name"]

    }