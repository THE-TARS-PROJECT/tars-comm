from dbus_fast.aio import MessageBus
from asyncio import run, create_task, Event
from dbus_fast.service import ServiceInterface, dbus_method, dbus_signal

from client_socket import ClientSock
from client_auth import Authenticator

class DBUSInterface(ServiceInterface):
    def __init__(self, name):
        super(DBUSInterface, self).__init__(name)

        self.config = Authenticator().read_config()
        self.client_id = self.config['ph_no']

        self.socket = ClientSock()
        self.socket._on_dial_req_response = self._on_call_response
        create_task(self.socket.connect(self.client_id))

    @dbus_method()
    async def dial_number(self, ph_no: 's') -> 's':
        await self.socket.dial_number(ph_no)
        return f"calling..... {ph_no}"
    
    async def _on_call_response(self, data):
        await self.on_call_response(data)
    
    @dbus_signal()
    def on_call_response(self, data: 'a{sv}') -> 'a{sv}': # type: ignore
        print("received a call response")
        print(data)
        return data
    
async def main():
    bus = await MessageBus().connect()
    inf = DBUSInterface("com.cooper.tars.interface")
    # print(await inf.call_dial_number("Hello, World"))
    bus.export("/cooper/tars/comm", inf)
    await bus.request_name("com.cooper.tars")
    await Event().wait()

run(main())
