from enum import Enum
from uuid import uuid4
from asyncio import create_task
from socketio.async_client import AsyncClient
from socketio.exceptions import ConnectionError, ConnectionRefusedError

from client_auth import Authenticator


class ServerEvents(Enum):
    SERVER_MESSAGE = "SERVER_MESSAGE"
    CALL_REQUEST_STATUS = "CALL_REQUEST_STATUS"
    REQUEST_CALL = "REQUEST_CALL"
    CALL_ACCEPTED = "CALL_ACCEPTED"
    CALL_REJECTED = "CALL_REJECTED"
    CALL_REQUEST = "CALL_REQUEST"
    AUDIO_PACKET_EMIT = "AUDIO_PACKET_EMIT" # server is emitting audio packets
    AUDIO_PACKET_RECV = "AUDIO_PACKET_RECV" # client is recving some audio packets


def load_test_token():
    with open("./test-token.txt", "r") as token:
        return token.read()


class ClientSock:
    def __init__(self, on_incoming_call: callable, on_audio_packet_recv: callable):
        super(ClientSock, self).__init__()

        self.sock = AsyncClient(reconnection=True, logger=True)
        self.active_room = ""
        self.auth = Authenticator()

        self._on_incoming_call = on_incoming_call
        self._on_audio_packet_recv = on_audio_packet_recv

        self.sock.on(ServerEvents.SERVER_MESSAGE.value, self.on_server_message)
        self.sock.on(ServerEvents.CALL_REQUEST.value, self.on_incoming_call)
        self.sock.on(ServerEvents.AUDIO_PACKET_RECV, self.on_audio_packet_recv)

    def on_server_message(self, data):
        print(f"SERVER_MESSAGE: {data.get('msg')}")

    async def connect(self, phone_no: str):
        try:
            access_token = self.auth.read_config()['access_token']

            await self.sock.connect(
                "https://545904031155.ngrok-free.app",
                auth={
                    "phone_no": phone_no,
                    "token": access_token
                },
                
                transports=["websocket"],
            )

            print("Connected to server")
            create_task(self.sock.wait())

        except ConnectionError as e:
            print(f"Unexpected connection error: {str(e)}")
            print("Revalidating JWT…")
            self.auth.login_with_token()

        except ConnectionRefusedError as e:
            print(f"Server rejected the connection: {str(e)}")

    async def disconnect(self):
        try:
            await self.sock.disconnect()
            print("Disconnected from server cleanly.")
        except Exception:
            pass

    async def on_incoming_call(self, data):
        if self._on_incoming_call:
            await self._on_incoming_call(data)

    async def dial_number(self, phone_no: str):
        await self.sock.emit(ServerEvents.REQUEST_CALL.value, {
            "target_phone_no": phone_no,
            "phone_no": self.auth.config['ph_no']
        })

    async def accept_call(self, target: str):
        self.active_room = uuid4()
        await self.sock.emit(ServerEvents.CALL_ACCEPTED.value, data={
            "room_id": str(self.active_room),
            "target": target
        })

    async def broadcast_audio_packet(self, packet: bytes):
        await self.sock.emit(ServerEvents.AUDIO_PACKET_EMIT.value, data={
            "packet": packet, 
            "room": self.active_room
        })

    async def on_audio_packet_recv(self, data):
        if self._on_audio_packet_recv:
            self._on_audio_packet_recv(data['packet'])
