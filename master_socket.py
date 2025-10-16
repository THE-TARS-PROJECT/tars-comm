from fastapi import FastAPI
from utils import ClientManager
from socketio import AsyncServer, ASGIApp

sock = AsyncServer(async_mode='asgi')
f_app = FastAPI()
app = ASGIApp(sock, f_app)

client_manager = ClientManager()

"""
connect

runs when a client connects 
only registered clients allowed
"""
@sock.event
async def connect(sid, environ, auth):
    client_manager.auth_client(auth['client_id'], auth['token'])
    await sock.emit("server_msg", data={'msg': 'connected'}, to=sid)
