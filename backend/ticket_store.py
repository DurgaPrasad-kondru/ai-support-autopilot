
# Shared mock ticket database.
# These are demonstration records, not a real support system.

tickets = {
    "TKT1001": {
        "status": "Resolved",
        "priority": "High",
        "assigned_to": "Support Team A",
    },
    "TKT1002": {
        "status": "In Progress",
        "priority": "Medium",
        "assigned_to": "Technical Team",
    },
    "TKT1003": {
        "status": "Escalated",
        "priority": "Critical",
        "assigned_to": "Billing Manager",
    },
}


def get_ticket_status(ticket_id: str) -> dict:
    """Return mock ticket details or an explicit not-found result."""
    ticket_id = ticket_id.strip().upper()

    ticket = tickets.get(ticket_id)

    if ticket is None:
        return {
            "error": "Ticket not found",
            "ticket_id": ticket_id,
        }

    return {
        **ticket,
        "ticket_id": ticket_id,
    }