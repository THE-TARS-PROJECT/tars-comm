# implementation with dbus - systemd service
from enum import Enum
from asyncio import run, CancelledError
from socketio.async_client import AsyncClient
from socketio.exceptions import ConnectionError, ConnectionRefusedError

from client_auth import Authenticator

class ServerEvents(Enum):
    SERVER_MESSAGE = "SERVER_MESSAGE" # Simple server message
    DIAL_REQ_RESP = "DIAL_REQ_RESP"


class ClientEvents(Enum):
    REQ_CALL = "REQUEST_CALL"


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

    async def connect(self, client_id: str):
        try:
            await self.sock.connect(
                "https://captainprice.hackclub.app",
                auth={
                    "client_id": client_id,
                    "token": load_test_token()
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
    def dial_number(self, phone_no: str):
        # self.sock.emit(ClientEvents.REQ_CALL, data={
        #     "phone_no": phone_no
        # })
        self.sock.emit("request_dial", data={
            "phone_no": phone_no
        })
        

"""
test
"""
# async def main():
#     cs = ClientSock()
#     await cs.connect("9582576830")


# try:
#     run(main())

# except CancelledError:
#     print("Closing the socket")
