import asyncio
import websockets
import re

# Server IP and Port
HOST = '0.0.0.0'
PORT = 61000

clients = set()

def format_message(msg, client_ip):
    """Format the message to include clickable links."""
    url_regex = r'(https?:\/\/[^\s]+)'  # Regex to match URLs
    formatted_msg = re.sub(url_regex, r'<a href="\g<0>" target="_blank">link</a>', msg)
    return f"[{client_ip}]: {formatted_msg}"

async def broadcast(message, sender_socket):
    """Broadcast the formatted message to all connected clients."""
    for client in clients:
        try:
            await client.send(message)
        except Exception as e:
            print(f"Error broadcasting to client: {e}")

async def handle_client(websocket, path):
    """Handle communication with a connected client."""
    clients.add(websocket)
    client_ip = websocket.remote_address[0]
    print(f"Client connected: {client_ip}")

    try:
        async for message in websocket:
            # Format the message to include the sender's IP address and clickable links
            formatted_message = format_message(message, client_ip)
            print(f"Received: {formatted_message}")
            await broadcast(formatted_message, websocket)  # Broadcast the formatted message
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
