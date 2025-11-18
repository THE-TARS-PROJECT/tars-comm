# implementation with dbus - systemd service
from pydbus import SessionBus
from gi.repository import GLib
from socketio import AsyncClient

class ClientService(AsyncClient):
    def __init__(self):
        super(ClientService, self).__init__()

        self.dbus_session = SessionBus()
        self.loop = GLib.Main_Loop()
        self.config = {}

        # connect to websocket
        try:
            self.connect(
                "captainprice.hackclub.app", auth={
                    "client_id": "",
                    "token": "",
                }
            )

        except Exception as e:
            pass

    def read_config(self):
        pass

