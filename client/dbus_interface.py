from dbus_fast.aio import MessageBus
from asyncio import run, create_task, Event
from dbus_fast.service import ServiceInterface, dbus_method, dbus_signal

from client_socket import ClientSock
from client_auth import Authenticator

from plyer import notification

class DBUSInterface(ServiceInterface):
    def __init__(self, name, socket: ClientSock = None):
        super(DBUSInterface, self).__init__(name)

        self.app_name = "TARS COMMUNICATION PROTOCOL"

        # ensure setting socket manually
        self.socket = socket

    """
    dial_number 

    tells the server to ping the target client
    requires:
    ph_no: str -> phone number of the target client 
    """
    @dbus_method()
    async def dial_number(self, ph_no: 's') -> 's': #type: ignore
        await self.socket.dial_number(ph_no)
        return f"calling..... {ph_no}"

    """
    incoming_call (signal)

    emitted when some client calls
    requires:
    who -> phone_no of target client

    by default wrapped under another function
     """
    @dbus_signal("incoming_call")
    def incoming_call(self, who) -> 's': # type: ignore
        print("signal emitted")
        return who


    """
    accept_call

    accepts the call
    """
    @dbus_method()
    def accept_call(self, target: 's') -> 's': #type:ignore
        print("call accpeted")
        self.socket.accept_call(
            self.socket.get_sid(),
            target
        )    

    def action_decline_call(self):
        print("call declined")
    
    async def _on_incoming_call(self, data):
        notification.notify(
            "INCOMING CALL...",
            f"{data['who']} is calling",
            self.app_name
        )
        self.incoming_call(data['who'])
    
async def exec_interface():
    bus = await MessageBus().connect()

    inf = DBUSInterface("com.cooper.tars.interface")
    sock = ClientSock(inf._on_incoming_call)
    
    inf.socket = sock
    await inf.socket.connect(sock.auth.config['ph_no'])
    # print(await inf.call_dial_number("Hello, World"))
    bus.export("/cooper/tars/comm", inf)
    await bus.request_name("com.cooper.tars")
    await Event().wait()



run(exec_interface())
