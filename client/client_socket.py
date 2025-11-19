# implementation with dbus - systemd service
from pydbus import SessionBus
from gi.repository import GLib
from socketio import AsyncClient

from client_auth import Authenticator

class ClientService(AsyncClient):
    def __init__(self):
        super(ClientService, self).__init__()

        self.dbus_session = SessionBus()
        self.loop = GLib.Main_Loop()

        self.auth = Authenticator()
        self.config = self.auth.read_config()


        # connect to websocket
        try:
            if self.config['name']:
                self.connect(
                    "captainprice.hackclub.com", auth={
                        "client_id": self.config['name'],
                        "token": self.config['access_token']
                    }
                )

        except Exception as e:
            print("failed to connect to server.", str(e))


# test
service = ClientService()

