from asyncio import Event, run
from dbus_fast.service import (
    ServiceInterface, dbus_method
)
from dbus_fast.aio import MessageBus
from client_socket import ClientService

class TarsComInterface(ServiceInterface):

    def __init__(self):
        super(TarsComInterface, self).__init__("com.cooper.tars")
        
        # self.sock = ClientService()
        # self.sock.connect_to_server()


    @dbus_method()
    async def on_call_requested(self, data: 's') -> 's':
        return f"hello, {data}"


async def main():
    bus = await MessageBus().connect()
    interface = TarsComInterface()
    bus.export("/com/cooper/tars", interface)
    await bus.request_name("com.cooper.tars")
    await Event().wait()


run(main())
