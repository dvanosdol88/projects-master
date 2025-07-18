#!/bin/bash
# Start the Queue API server

echo "🚀 Starting Queue API Server..."

# Kill any existing process on port 5006
lsof -ti:5006 | xargs kill -9 2>/dev/null || true

# Start the server
/mnt/c/Users/david/projects-master/venv/bin/python queue_api_server.py