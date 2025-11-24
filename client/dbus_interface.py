from dbus_fast.aio import MessageBus
from asyncio import run, create_task, Event
from dbus_fast.service import ServiceInterface, dbus_method, dbus_signal

from client_socket import ClientSock
from client_auth import Authenticator

from plyer.facades import Notification

class DBUSInterface(ServiceInterface):
    def __init__(self, name):
        super(DBUSInterface, self).__init__(name)

        self.config = Authenticator().read_config()
        self.client_id = self.config['ph_no']

        self.notifyer = Notification()

        self.socket = ClientSock()
        self.socket._on_incoming_call = self.on_incoming_call
    
        create_task(self.socket.connect(self.client_id))

    @dbus_method()
    async def dial_number(self, ph_no: 's') -> 's':
        await self.socket.dial_number(ph_no)
        return f"calling..... {ph_no}"
    
    async def on_incoming_call(self, data):
        print("DBUS GOT THE INCOMING CALL")
    
async def exec_interface():
    bus = await MessageBus().connect()
    inf = DBUSInterface("com.cooper.tars.interface")
    # print(await inf.call_dial_number("Hello, World"))
    bus.export("/cooper/tars/comm", inf)
    await bus.request_name("com.cooper.tars")
    await Event().wait()



run(exec_interface())