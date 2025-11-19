# implementation with dbus - systemd service
from asyncio import run
from socketio import AsyncClient
from jeepney import DBusAddress, new_method_call
from jeepney.io.asyncio import open_dbus_connection

from client_auth import Authenticator

def load_test_token() -> str:
    with open("./test-token.txt", "r") as token:
        token_ = token.read()
        return token_

class ClientService(AsyncClient):
    def __init__(self):
        super(ClientService, self).__init__()

        # self.dbus_session = DBusAddress()
        # self.con = open_dbus_connection(bus="SESSION")

        self.auth = Authenticator()
        self.config = self.auth.read_config()

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


async def main():
    service = ClientService()
    await service.connect_to_server()

if __name__ == "__main__":
    run(main())    
