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
from mcp.types import ToolAnnotations


mcp = FastMCP("booking-server")


@mcp.tool(
    name="create_booking",
    title="Create booking",
    description=(
        "Create a booking record with the given booking ID. "
        "Use this when the user wants to create or register a new booking. "
        "Provide a single booking_id string; returns a JSON object indicating success and echoing the ID."
    ),
    annotations=ToolAnnotations(
        title="Create booking",
        readOnlyHint=False,
        openWorldHint=False,
    ),
    meta={
        "capabilities": ["booking", "reservation", "write", "create"],
        "request_schema": {
            "booking_id": "string (required). Unique identifier for the booking to create.",
        },
        "response_schema": {
            "status": 'string. "success" if the booking was created.',
            "booking_id": "string. Echo of the provided booking_id.",
            "error": "string (optional). Present only if booking creation failed.",
        },
    },
    structured_output=True,
)
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


