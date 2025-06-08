import asyncio
import websockets
from datetime import datetime

# Store connected clients and light status
connected_clients = set()
light_status1 = "0"  # Initial state: light off

async def handler(websocket):
    global light_status1
    connected_clients.add(websocket)
    print(f"New client connected. Total clients: {len(connected_clients)}")
    

    # Send current light status immediately upon connection
    await websocket.send(light_status1)

    try:
        async for message in websocket:
            if message in ("0", "1"):
                if message != light_status1:
                    light_status1 = message
                    print(f"Light 1 status changed to {light_status1}")                   
                    # Broadcast new status to all clients
                    await asyncio.gather(*[
                        client.send(light_status1)
                        for client in connected_clients
                        ])
                    if light_status1 == "0":
                        # Here you would add Modbus control to turn off light 1
                        print(0)
                    else:
                        # Here you would add Modbus control to turn on light 1
                        print(1)

                elif message == light_status1:
                    await asyncio.gather(*[
                        client.send("is "+light_status1)
                        for client in connected_clients
                        ])

            else:
                print(f"Received invalid command: {message}")
                await websocket.send("invalid command")


    finally:
        connected_clients.remove(websocket)
        print(f"Client disconnected. Remaining clients: {len(connected_clients)}")

# Get current light status every 10 seconds
async def get_current_light_status():
    while True:
        # Here you would add Modbus logic to get current light status
        await asyncio.sleep(10)
        #light_status1 = "0"  # Initial state: light off

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
        asyncio.create_task(get_current_light_status())
        asyncio.create_task(send_server_messages())
        print("WebSocket server started on ws://localhost:8765")
        print("Initial light status: 0 (OFF)")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())