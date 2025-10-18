#!/bin/bash

# Ensure the FastMCP server uses the internal port (9000) expected by app.py
export MCP_PORT=9000

# 1. Start the FastMCP backend server on internal port 9000.
# The '&' sends the process to the background, allowing the next command to run.
echo "Starting FastMCP Server on 0.0.0.0:$MCP_PORT..."
python server.py &

# 2. Start the Chainlit application on the external port provided by Railway ($PORT).
echo "Starting Chainlit Frontend on 0.0.0.0:$PORT..."
chainlit run app.py --host 0.0.0.0 --port $PORT

# Wait for all background jobs to finish (optional, but ensures the container stays alive)
wait
