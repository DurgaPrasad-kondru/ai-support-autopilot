from mcp.server import Server

mcp = Server("SupportTools")

@mcp.tool()
def ticket_status(ticket_id: str):

    return f"Ticket {ticket_id} is currently in progress"

if __name__ == "__main__":
    mcp.run()