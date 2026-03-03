"""
Minimal FastMCP-based MCP server exposing a single `create_booking` tool.

Instructions
------------
1. Create and activate a virtual environment (optional but recommended):

   python -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\\Scripts\\activate

2. Install dependencies:

   pip install fastmcp

3. Run the server:

   python booking_server.py

The server will start an HTTP MCP server on 0.0.0.0:9001, exposing a single
tool named `create_booking` at the `/mcp` path.
"""

from fastmcp import FastMCP


mcp = FastMCP("booking-server")


@mcp.tool
async def create_booking(booking_id: str) -> dict:
    """
    Create a booking with the given ID.

    Parameters
    ----------
    booking_id : str
        The ID of the booking to create.

    Returns
    -------
    dict
        JSON-serializable response:
        {
          "status": "success",
          "booking_id": "<passed_booking_id>"
        }
    """
    return {
        "status": "success",
        "booking_id": booking_id,
    }


if __name__ == "__main__":
    # Run FastMCP over HTTP on port 9001
    mcp.run(transport="http", host="0.0.0.0", port=9001)


