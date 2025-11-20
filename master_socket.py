from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from socketio import AsyncServer, ASGIApp
from utils import ClientManager, CLIENT_STATUS

from enum import Enum

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

class Events(Enum):
    SERVER_MESSAGE = "SERVER_MESSAGE" # Simple server message
    CALL_REQUEST_STATUS = "CALL_REQUEST_STATUS" # Tells the client about the status of call request
    REQUEST_CALL = "REQUEST_CALL" # A is client is requesting the server to call another client
    CALL_ACCEPTED = "CALL_ACCEPTED" # The client has accepted the call, server will put both in a room
    CALL_REJECTED = "CALL_REJECTED" # The client rejected the call

"""
connect

runs when a client connects 
only registered clients allowed
"""
@sock.event
async def connect(sid, environ, auth):
    if client_manager.auth_client(auth['client_id'], auth['token']):
        await sock.emit(Events.SERVER_MESSAGE, data={'msg': 'connected'}, to=sid)
    else:
        await sock.emit(Events.SERVER_MESSAGE, data={"msg": "failed to connect"}, to=sid)


"""
handle_dial

client socket emits "request_dial"
"""
@sock.on("request_dial")
def on_dial_requested(sid, data):
    if client_manager.client_lookup(data['phone_no']) == CLIENT_STATUS.OFFLINE:
        sock.emit(Events.CALL_REQUEST_STATUS, data={"msg": "request client not available"}, to=sid)
        
