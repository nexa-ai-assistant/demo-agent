"""
Minimal MCP SDK FastMCP server exposing a single `create_booking` tool.

Instructions
------------
1. Create and activate a virtual environment (optional but recommended):

   python -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\\Scripts\\activate

2. Install dependencies (MCP SDK server extras):

   pip install "mcp[server]"

3. Run the server:

   # stdio transport (e.g. for local MCP clients)
   MCP_TRANSPORT=stdio python booking_server.py

   # HTTP/streamable transport on port 9001
   MCP_TRANSPORT=streamable-http PORT=9001 python booking_server.py

The server will start an MCP server on 0.0.0.0:9001 (when using streamable-http),
exposing a single tool named `create_booking` at the root (`/`) path.
"""

import os
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations


_port = int(os.environ.get("PORT", "9001"))
mcp = FastMCP(
    "Booking Server",
    json_response=True,
    host="0.0.0.0",
    port=_port,
    streamable_http_path="/",
)


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
async def create_booking(booking_id: str) -> dict[str, Any]:
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


def main() -> None:
    """
    Run the MCP server using the configured transport.

    Set MCP_TRANSPORT to either:
    - "stdio"           for stdio-based MCP clients, or
    - "streamable-http" for HTTP on 0.0.0.0:PORT (default 9001).
    """
    transport = os.environ.get("MCP_TRANSPORT", "streamable-http")
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()

