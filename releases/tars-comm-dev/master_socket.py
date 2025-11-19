from fastapi import FastAPI
from socketio import AsyncServer, ASGIApp
from utils import ClientManager, CLIENT_STATUS


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


"""
handle_dial

connection does not automatically call the the target.
client must emit dial with target_client_id to connect to another socket.
"""
@sock.event
async def handle_dial(sid, data):
    print(f"received dial request from: {sid}")
    if client_manager.client_lookup(data['target_client_id']) == CLIENT_STATUS.ONLINE:
        await sock.emit("call_req", data={
            "req_client_id": sid
        }, to=sid)

    else:
        await sock.emit("call_resp", data={
            "msg": "target client not available"
        }, to=sid)
