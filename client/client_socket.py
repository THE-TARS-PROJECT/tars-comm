from enum import Enum
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


def load_test_token():
    with open("./test-token.txt", "r") as token:
        return token.read()


class ClientSock:
    def __init__(self):
        self.sock = AsyncClient(reconnection=True, logger=True)
        self.auth = Authenticator()

        
        self._on_dial_req_response = None

    def set_on_dial_request_response(self, callback):
        self._on_dial_req_response = callback

    async def connect(self, phone_no: str):
        try:
            access_token = self.auth.read_config()['access_token']

            self.sock.handlers.clear()

            self.sock.on(ServerEvents.SERVER_MESSAGE.value, self.on_server_message)
            self.sock.on(ServerEvents.CALL_REQUEST_STATUS.value, self.on_dial_req_status)
            # ensure we handle incoming call notifications
            self.sock.on(ServerEvents.CALL_REQUEST.value, self.on_call_request)

            await self.sock.connect(
                # "https://c6955500d65d.ngrok-free.app",
                "https://411c646d4018.ngrok-free.app",
                auth={
                    "phone_no": phone_no,
                    "token": access_token
                },
                # prefer raw websocket transport when behind proxies
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
        """Call when your app closes to avoid queued events."""
        try:
            await self.sock.disconnect()
            print("Disconnected from server cleanly.")
        except Exception:
            pass

    def on_server_message(self, data):
        print(f"SERVER_MESSAGE: {data.get('msg')}")

    def on_dial_req_status(self, data):
        print(data)
        if self._on_dial_req_response:
            self._on_dial_req_response(data)
        else:
            print("CALL_REQUEST_STATUS received but no handler set:", data)

    def on_call_request(self, data):
        # handler for incoming call request from server
        print("INCOMING CALL:", data)

    async def dial_number(self, phone_no: str):
        await self.sock.emit(ServerEvents.REQUEST_CALL.value, {
            "phone_no": phone_no
        })
