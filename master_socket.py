from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from socketio import AsyncServer, ASGIApp
from utils import ClientManager, CLIENT_STATUS

from enum import Enum
from uvicorn import run

from auth_router import auth_router, s_client

class ServerEvents(Enum):
    SERVER_MESSAGE = "SERVER_MESSAGE" # Simple server message
    CALL_REQUEST_STATUS = "CALL_REQUEST_STATUS" # Tells the client about the status of call request
    REQUEST_CALL = "REQUEST_CALL" # A is client is requesting the server to call another client
    CALL_ACCEPTED = "CALL_ACCEPTED" # The client has accepted the call, server will put both in a room
    CALL_REJECTED = "CALL_REJECTED" # The client rejected the call
    CALL_REQUEST = "CALL_REQUEST" # Server tells the client b that a call is incoming

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


@sock.event
async def connect(sid, environ, auth):
    if client_manager.auth_client(auth['phone_no'], auth['token']):
        await sock.emit(
            ServerEvents.SERVER_MESSAGE.value, {"msg": "connected"}, to=sid
        )
    else:
        sock.disconnect(sid)


def on_client_requests_call(sid, data):
    print(f'received request from {sid}')
    client_status = client_manager.client_lookup(data['phone_no'])
    print(client_status)
    if client_status == CLIENT_STATUS.BUSY or client_status == CLIENT_STATUS.ONLINE:
        sock.emit(ServerEvents.CALL_REQUEST_STATUS.value, data={
            "msg": client_status.value
        }, to=sid)

        sock.emit(ServerEvents.CALL_REQUEST, data={
            "who": sid
        }, to=client_manager.get_client_sid(data['phone_no']))

sock.on(ServerEvents.REQUEST_CALL.value, on_client_requests_call)