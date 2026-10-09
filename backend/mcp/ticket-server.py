from fastmcp import FastMCP

mcp = FastMCP("Ticket Server")

# ---------- MOCK TICKET DATABASE ----------

tickets = {

    "TKT1001": {

        "status": "Resolved",
        "priority": "High",
        "assigned_to": "Support Team A"

    },

    "TKT1002": {

        "status": "In Progress",
        "priority": "Medium",
        "assigned_to": "Technical Team"

    },

    "TKT1003": {

        "status": "Escalated",
        "priority": "Critical",
        "assigned_to": "Billing Manager"

    }

}


# ---------- MCP TOOL ----------

@mcp.tool()
def get_ticket_status(ticket_id: str):

    """
    Fetch ticket details using ticket ID
    """

    return tickets.get(

        ticket_id,

        {
            "error": "Ticket not found"
        }

    )


# ---------- RUN MCP SERVER ----------

if __name__ == "__main__":

    mcp.run()