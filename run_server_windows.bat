@echo off
echo Starting Flask server...
start cmd /k "python flask_server.py"

echo Starting WebSocket server...
start cmd /k "python websocket_server.py"

pause
