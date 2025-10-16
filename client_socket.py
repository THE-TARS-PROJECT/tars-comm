import asyncio
import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("✅ Connected to master socket")

@sio.event
async def server_msg(data):
    pass

@sio.event
async def pong_client(data):
    print("📨 Pong:", data)

@sio.event
async def disconnect():
    print("❌ Disconnected from server")

async def main():
    with open("token.txt", "r") as token_file:
        token = token_file.read()
        token_file.close()
    await sio.connect(
        "http://localhost:8000",
        auth={"token": token, "client_id": "+91 95828576830"}  # 🔐 Auth header sent here
    )

    await sio.emit("ping_server", {"msg": "Hello, Master!"})
    await asyncio.sleep(3)
    await sio.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
