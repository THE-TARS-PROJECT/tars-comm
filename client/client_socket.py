# implementation with dbus - systemd service
from asyncio import run
from socketio.async_client import AsyncClient
from jeepney import DBusAddress, new_method_call
from jeepney.bus_messages import message_bus
from jeepney.io.asyncio import open_dbus_connection

from client_auth import Authenticator

def load_test_token() -> str:
    with open("./test-token.txt", "r") as token:
        token_ = token.read()
        return token_

class ClientService(AsyncClient):
    def __init__(self):
        super(ClientService, self).__init__()

        self.dbus_session = DBusAddress(
            object_path="/com/cooper/tars/com",
            bus_name="com.cooper.tars",
            interface="com.cooper.tars.Interface"
        )
    
        self.auth = Authenticator()
        self.config = self.auth.read_config()

        self.conn = None

    async def start_dbus(self):
        self.conn = await open_dbus_connection("SESSION")
        message_bus.RequestName("com.cooper.tars")

        while True:
            msg = await self.conn.receive()
            header = msg.header

    async def connect_to_server(self):
        try:
            await self.connect(
                "https://captainprice.hackclub.app",
                auth={
                    "client_id": self.config['ph_no'],
                    "token": load_test_token()
                }
            )

            await self.wait()

        except Exception as error:
            print("failed to connect to the server", str(error))

        finally:
            if self.connected:
                self.disconnect()

    async def dial_number(self, number: str):
        pass

    @AsyncClient.on("call_req")
    def on_call_req(self, data):
        if data['msg'] == "target client not available":
            print("you got it boss")


async def main():
    service = ClientService()
    await service.connect_to_server()

if __name__ == "__main__":
    run(main())    
