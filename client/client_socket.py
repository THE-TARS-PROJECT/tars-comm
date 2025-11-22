# implementation with dbus - systemd service
from enum import Enum
from asyncio import run, CancelledError
from socketio.async_client import AsyncClient
from socketio.exceptions import ConnectionError, ConnectionRefusedError

from client_auth import Authenticator

class ServerEvents(Enum):
    SERVER_MESSAGE = "SERVER_MESSAGE" # Simple server message
    CALL_REQUEST_STATUS = "CALL_REQUEST_STATUS" # Tells the client about the status of call request
    REQUEST_CALL = "REQUEST_CALL" # A is client is requesting the server to call another client
    CALL_ACCEPTED = "CALL_ACCEPTED" # The client has accepted the call, server will put both in a room
    CALL_REJECTED = "CALL_REJECTED" # The client rejected the call
    CALL_REQUEST = "CALL_REQUEST" # Server tells the client b that a call is incoming


def load_test_token():
    with open("./test-token.txt", "r") as token:
        token_ = token.read()
        return token_

class ClientSock:
    def __init__(self):
        super(ClientSock, self).__init__()
        
        self.sock = AsyncClient(reconnection=False, logger=True)
        self.auth = Authenticator()

        # self.sock.on(Events.SERVER_MESSAGE, self.on_server_message)
        self.sock.on("server_msg", self.on_server_message)
        self.sock.on("call_resp", self.on_dial_req_response)

    async def connect(self, phone_no: str):
        try:
            access_token = self.auth.read_config()['access_token']
            await self.sock.connect(
                "https://2da2e6c44a7c.ngrok-free.app",
                auth={
                    "phone_no": phone_no,
                    "token": access_token
                }
            )
            self.sock.logger.info("Connected to server")
            print("Connected to server")
            
            await self.sock.wait()

        except ConnectionError as con_error:
            self.sock.logger.error(f"An unexpected error occurred while connecting to the server: {str(con_error)}")
            print(f"An unexpected error occurred while connecting to the server: {str(con_error)}")

        except ConnectionRefusedError as con_refused:
            self.sock.logger.error(f"Server refused the connection: {str(con_refused)}")
            print(f"Server refused the connection: {str(con_refused)}")

    """
    functions below are receivers
    server -> client
    """

    def on_server_message(self, data):
        print(data['msg'])

    def on_dial_req_response(self, data):
        print(data['msg'])

    
    """
    functions below are emitters 
    client -> server
    """
    async def dial_number(self, phone_no: str):
        await self.sock.emit(ServerEvents.REQUEST_CALL.value, data={
            "phone_no": phone_no
        })
        