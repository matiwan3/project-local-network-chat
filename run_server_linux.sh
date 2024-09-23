#!/bin/bash

# Run Flask server in the background
echo "Starting Flask server..."
python flask_server.py &

# Run WebSocket server in the background
echo "Starting WebSocket server..."
python websocket_server.py &

# Wait for background processes to finish (optional, so they can be terminated manually with Ctrl+C)
wait