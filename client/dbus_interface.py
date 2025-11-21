from dbus_fast.aio import MessageBus
from asyncio import run, create_task, Event
from asyncio.exceptions import CancelledError
from dbus_fast.service import ServiceInterface, dbus_method

from client_socket import ClientSock
from client_auth import Authenticator

class DBUSInterface(ServiceInterface):
    def __init__(self, name):
        super(DBUSInterface, self).__init__(name)

        self.config = Authenticator().read_config()
        self.client_id = self.config['ph_no']

        self.socket = ClientSock()
        create_task(self.socket.connect(self.client_id))

    @dbus_method()
    def dial_number(self, ph_no: 's') -> 's':
        self.socket.dial_number(ph_no)
        print(f"calling..... {ph_no}")
        return f"calling..... {ph_no}"
    
async def main():
    bus = await MessageBus().connect()
    inf = DBUSInterface("com.cooper.tars.interface")
    bus.export("/cooper/tars/comm", inf)
    await bus.request_name("com.cooper.tars")
    await Event().wait()

run(main())
