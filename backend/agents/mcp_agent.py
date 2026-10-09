
import re

from ticket_store import get_ticket_status


def mcp_agent(state):
    question = state["question"]

    match = re.search(r"\bTKT\d+\b", question, re.IGNORECASE)

    if match:
        ticket_id = match.group().upper()
        ticket_data = get_ticket_status(ticket_id)

        if ticket_data.get("error"):
            tool_context = (
                f"Ticket ID: {ticket_id}\n"
                "Status: Ticket not found in the demonstration database."
            )
        else:
            tool_context = (
                f"Ticket ID: {ticket_data['ticket_id']}\n"
                f"Status: {ticket_data['status']}\n"
                f"Priority: {ticket_data['priority']}\n"
                f"Assigned To: {ticket_data['assigned_to']}"
            )
    else:
        tool_context = ""

    return {
        "tool_context": tool_context,
        "question": question,
        "email": state["email"],
        "name": state["name"],
        "route": state.get("route"),
    }