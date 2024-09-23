import asyncio
import websockets

# Server IP and Port (use '0.0.0.0' to make the server accessible from other devices on the local network)
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 61000

clients = set()

async def broadcast(message, sender_socket):
    """Broadcast the message to all connected clients, including the sender."""
    if clients:
        print(f"Broadcasting message: {message} to {len(clients)} clients")
    for client in clients:
        try:
            await client.send(message)
        except Exception as e:
            print(f"Error broadcasting to client: {e}")

async def handle_client(websocket, path):
    """Handle communication with a connected client."""
    clients.add(websocket)
    client_ip = websocket.remote_address[0]  # Get the client's IP address
    print(f"Client connected: {client_ip}")

    try:
        async for message in websocket:
            # Prepend the sender's IP address to the message
            message_with_ip = f"[{client_ip}]: {message}"
            print(f"Received: {message_with_ip}")
            await broadcast(message_with_ip, websocket)  # Broadcast the message to all clients
    finally:
        clients.remove(websocket)
        print(f"Client disconnected: {client_ip}")

async def start_server():
    """Start the WebSocket server."""
    server = await websockets.serve(handle_client, HOST, PORT)
    print(f"WebSocket server running on ws://{HOST}:{PORT}")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())
