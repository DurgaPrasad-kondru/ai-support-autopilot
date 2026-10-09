import re

try:
    from mcp.ticket_server import get_ticket_status
except (ImportError, ModuleNotFoundError):
    def get_ticket_status(ticket_id):
        return {}


def mcp_agent(state):

    question = state["question"]

    pattern = r"TKT\d+"

    match = re.search(
        pattern,
        question
    )

    if match:

        ticket_id = match.group()

        ticket_data = get_ticket_status(
            ticket_id
        )

        tool_context = f"""

        Ticket ID: {ticket_id}

        Status: {ticket_data.get('status')}

        Priority: {ticket_data.get('priority')}

        Assigned To: {ticket_data.get('assigned_to')}

        """

    else:

        tool_context = ""

    return {

        "tool_context": tool_context,
        "question": state["question"],
        "email": state["email"],
        "name": state["name"],
        "route": state.get("route")

    }