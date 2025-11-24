from dbus_fast.aio import MessageBus
from asyncio import run, create_task, Event
from dbus_fast.service import ServiceInterface, dbus_method, dbus_signal

from client_socket import ClientSock
from client_auth import Authenticator

from notify2 import Notification, init

class DBUSInterface(ServiceInterface):
    def __init__(self, name, socket: ClientSock = None):
        super(DBUSInterface, self).__init__(name)

        self.app_name = "TARS COMMUNICATION PROTOCOL"
        init(self.app_name)
        # ensure setting socket manually
        self.socket = socket

    @dbus_method()
    async def dial_number(self, ph_no: 's') -> 's': #type: ignore
        await self.socket.dial_number(ph_no)
        return f"calling..... {ph_no}"
    
    async def on_incoming_call(self, data):
        Notification(
            "INCOMING CALL....",
            f"{data['who']} is calling",
            "notification-message-IM"
        ).show()
    
async def exec_interface():
    bus = await MessageBus().connect()

    inf = DBUSInterface("com.cooper.tars.interface")
    sock = ClientSock(inf.on_incoming_call)
    
    inf.socket = sock
    await inf.socket.connect(sock.auth.config['ph_no'])
    # print(await inf.call_dial_number("Hello, World"))
    bus.export("/cooper/tars/comm", inf)
    await bus.request_name("com.cooper.tars")
    await Event().wait()



run(exec_interface())