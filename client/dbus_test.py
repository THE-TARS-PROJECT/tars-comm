from dbus_fast.aio import MessageBus
import asyncio

async def main():
    bus = await MessageBus().connect()
    introspection = await bus.introspect("com.cooper.tars", "/com/cooper/tars")
    obj = bus.get_proxy_object("com.cooper.tars", "/com/cooper/tars", introspection)
    iface = obj.get_interface("com.cooper.tars")

    result = await iface.call_on_call_requested("cooper")
    print(result)


asyncio.run(main())