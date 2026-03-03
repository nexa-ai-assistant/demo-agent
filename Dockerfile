FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (if needed) and create a non-root user (optional)
RUN pip install --no-cache-dir --upgrade pip

# Copy application code
COPY booking_server.py /app/booking_server.py

# Install Python dependencies (MCP SDK server extras).
RUN pip install --no-cache-dir "mcp[server]"

# Expose MCP server port
EXPOSE 9001

# Run the MCP server
CMD ["python", "booking_server.py"]

