import asyncio
import websockets
from datetime import datetime

# Store connected clients and light status
connected_clients = set()
light_status = "0"  # Initial state: light off

async def handler(websocket):
    global light_status
    connected_clients.add(websocket)
    print(f"New client connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            print(f"Received: {message}")
            
            if message == "0":
                if light_status == "0":
                    await websocket.send("is 0")
                else:
                    light_status = "0"
                    # Here you would add Modbus control to turn off light 1
                    await websocket.send("changed to 0")
                    
            elif message == "1":
                if light_status == "1":
                    await websocket.send("is 1")
                else:
                    light_status = "1"
                    # Here you would add Modbus control to turn on light 1
                    await websocket.send("changed to 1")
                    
            else:
                await websocket.send("invalid command")

    finally:
        connected_clients.remove(websocket)
        print(f"Client disconnected. Remaining clients: {len(connected_clients)}")

async def send_server_messages():
    """Send periodic messages from the server"""
    while True:
        await asyncio.sleep(10)  # Send every 10 seconds
        if connected_clients:
            message = f"Server message: {datetime.now().strftime('%H:%M:%S')}"
            print(f"Sending: {message}")
            await asyncio.gather(*[
                client.send(message)
                for client in connected_clients
            ])


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        # Start server message task
        asyncio.create_task(send_server_messages())
        print("WebSocket server started on ws://localhost:8765")
        print("Initial light status: 0 (OFF)")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())