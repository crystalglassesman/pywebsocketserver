import asyncio
import websockets
from datetime import datetime

# Store connected clients
connected_clients = set()

async def handler(websocket):
    # Add new client
    connected_clients.add(websocket)
    print(f"New client connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            # Display received message
            print(f"Received: {message}")
            
            # Broadcast message to all connected clients
            await asyncio.gather(*[
                client.send(f"{datetime.now().strftime('%H:%M:%S')} - {message}")
                for client in connected_clients
            ])
    finally:
        # Remove client when disconnected
        connected_clients.remove(websocket)
        print(f"Client disconnected. Remaining clients: {len(connected_clients)}")

async def send_server_messages():
    """Send periodic messages from the server"""
    while True:
        await asyncio.sleep(1)  # Send every 1 seconds
        if connected_clients:
            message = f"Server message: {datetime.now().strftime('%H:%M:%S')}"
            print(f"Sending: {message}")
            await asyncio.gather(*[
                client.send(message)
                for client in connected_clients
            ])

async def main():
    # Start WebSocket server
    async with websockets.serve(handler, "localhost", 8765):
        # Start server message task
        asyncio.create_task(send_server_messages())
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())