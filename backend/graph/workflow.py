from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.router_agent import router_agent
from agents.mcp_agent import mcp_agent
from agents.rag_agent import rag_agent
from agents.answer_agent import answer_agent
from agents.escalation_agent import escalation_agent


class GraphState(TypedDict):

    question: str
    context: str
    tool_context: str
    answer: str
    route: str
    escalated: bool
    email: str
    name: str


workflow = StateGraph(GraphState)

# ---------- NODES ----------

workflow.add_node(
    "router",
    router_agent
)

workflow.add_node(
    "mcp",
    mcp_agent
)

workflow.add_node(
    "rag",
    rag_agent
)

workflow.add_node(
    "answer",
    answer_agent
)

workflow.add_node(
    "escalation",
    escalation_agent
)

# ---------- FLOW ----------

workflow.set_entry_point("router")

workflow.add_edge(
    "router",
    "mcp"
)

workflow.add_edge(
    "mcp",
    "rag"
)

workflow.add_edge(
    "rag",
    "answer"
)

workflow.add_edge(
    "answer",
    "escalation"
)

workflow.add_edge(
    "escalation",
    END
)

# ---------- COMPILE ----------

app = workflow.compile()