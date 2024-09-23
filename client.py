import asyncio
import websockets

# Server IP and Port
HOST = '192.168.1.83'
PORT = 61000

# List of connected clients
clients = set()

async def broadcast(message, sender_socket):
    """Broadcast message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            await client.send(message)

async def handle_client(websocket, path):
    """Handle communication with a connected client."""
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")  # Log the message received
            await broadcast(message, websocket)
    finally:
        clients.remove(websocket)


async def start_server():
    """Start the WebSocket server."""
    server = await websockets.serve(handle_client, HOST, PORT)
    print(f"WebSocket server running on ws://{HOST}:{PORT}")
    await server.wait_closed()

# Start the server
if __name__ == "__main__":
    asyncio.run(start_server())
