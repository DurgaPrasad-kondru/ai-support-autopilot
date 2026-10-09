from fastmcp import FastMCP

mcp = FastMCP("SupportTools")

@mcp.tool()
def ticket_status(ticket_id: str):

    return f"Ticket {ticket_id} is currently under review"

@mcp.tool()
def customer_tier(email: str):

    return f"{email} belongs to Enterprise Plan"

@mcp.tool()
def active_incidents():

    return "Payment gateway latency issue detected"

if __name__ == "__main__":
    mcp.run()