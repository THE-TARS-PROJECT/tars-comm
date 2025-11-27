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
        return ph_no

    """
    incoming_call (signal)

    emitted when some client calls
    requires:
    who -> phone_no of target client

    by default wrapped under another function
     """
    @dbus_signal("incoming_call")
    def incoming_call(self, who) -> 's': # type: ignore
        return who


    """
    accept_call

    accepts the call
    """
    @dbus_method()
    async def accept_call(self): #type:ignore
        print(f"target phone no: {self.active_target}")
        await self.socket.accept_call(
            self.socket.sock.get_sid(),
            self.active_target
        )

    """
    send_audio_packet

    sends audio packet to room 
    """
    @dbus_method()
    async def send_audio_packet(self, packet: 'ay'):
        print("got some audio stuff")
        await self.socket.send_audio_packet(packet)

    @dbus_method()
    async def get_active_target(self) -> 's':
        return self.active_target

    def action_decline_call(self):
        self.active_target = None
        print("call declined")
    
    async def _on_incoming_call(self, data):
        notification.notify(
            "INCOMING CALL...",
            f"{data['who']} is calling",
            self.app_name
        )
        self.active_target = data['who']
        print(f"{data['who']} is calling - incoming call debug")
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
