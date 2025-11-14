from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth_router import s_client
from auth_router import auth_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), "static")

templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)

@app.get("/dashboard")
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
