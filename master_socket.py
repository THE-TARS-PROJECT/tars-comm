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
    AUDIO_PACKET_EMIT = "AUDIO_PACKET_EMIT" # server is emitting audio packets

sock = AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*",
    ping_interval=25,
    ping_timeout=60,
)

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
    if client_manager.auth_client(str(sid), auth['phone_no'], auth['token']):
        print(client_manager.clients)
        await sock.emit(
            ServerEvents.SERVER_MESSAGE.value, {"msg": "connected"}, to=sid
        )
    else:
        sock.disconnect(sid)

@sock.event
async def disconnect(sid, reason):
    print(f"Disconnected {sid}")
    client_manager.remove_client(sid)
    print(client_manager.clients)


async def on_client_requests_call(sid, data):
    phone_no = data.get('target_phone_no')
    print(f"Target phone no: {phone_no}")
    client_status = client_manager.client_lookup(phone_no)
    print(client_status)
    if client_status == CLIENT_STATUS.BUSY or client_status == CLIENT_STATUS.ONLINE:
        await sock.emit(ServerEvents.CALL_REQUEST_STATUS.value, data={
            "msg": str(client_status.value)
        }, to=sid)

        await sock.emit(ServerEvents.CALL_REQUEST.value, data={
            "msg": "incoming call",
            "who": data['phone_no']
        }, to=client_manager.get_sid_by_phone_no(data['target_phone_no']))


# for my ref - sid, is sid of acceptor
# to is requestor
async def on_client_accepted_call(sid, data):
    print("accepting call")
    target_sid = client_manager.get_sid_by_phone_no(data['target'])
    await sock.emit(ServerEvents.CALL_ACCEPTED.value, data={
                "room": data["room_id"]
            }, to=target_sid)

    await sock.enter_room(sid, data["room_id"])
    await sock.enter_room(target_sid, data['room_id'])

    print(f"{sid}: client sid")
    print(f"{target_sid}: target sid")

    client_manager.update_room(sid, data['room_id'])
    client_manager.update_room(target_sid, data['room_id'])

    print(client_manager.clients)

async def on_audio_packet_received(sid, data):
    print("getting audio pakcets")
    await sock.emit(AUDIO_PACKET_EMIT.value, skip_sid=sid, data={
            "audio_packet": "audio packet"
        })


sock.on(ServerEvents.CALL_ACCEPTED.value, on_client_accepted_call)
sock.on(ServerEvents.REQUEST_CALL.value, on_client_requests_call)
sock.on(ServerEvents.AUDIO_PACKET_EMIT.value, on_audio_packet_received)
sock.on("disconnect", disconnect)
