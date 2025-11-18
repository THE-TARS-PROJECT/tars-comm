from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from socketio import AsyncServer, ASGIApp
from utils import ClientManager, CLIENT_STATUS

from auth_router import auth_router, s_client


sock = AsyncServer(async_mode='asgi')
f_app = FastAPI()
app = ASGIApp(sock, f_app)

client_manager = ClientManager()

# merging registry and socket in one app
f_app.mount("/static", StaticFiles(directory="static"), "static")

templates = Jinja2Templates(directory="templates")

f_app.include_router(auth_router)

@f_app.get("/dashboard")
def dashboard(request: Request):
    user = s_client.auth.get_user(request.cookies.get("token")).user.user_metadata
    print(user)
    return templates.TemplateResponse(
        request, name='dashboard.html',
        context={
            "name": user.get("name"),
            "ph_no": user.get("ph_no")
        }
    )


"""
connect

runs when a client connects 
only registered clients allowed
"""
@sock.event
async def connect(sid, environ, auth):
    if client_manager.auth_client(auth['client_id'], auth['token']):
        await sock.emit("server_msg", data={'msg': 'connected'}, to=sid)
    else:
        await sock.emit("server_msg", data={'msg': 'failed'}, to=sid)


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
