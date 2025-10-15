from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from supabase import Client

auth_router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory="templates")

@auth_router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request, name='home.html', context={'title': "Home"}
    )

@auth_router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse(
        request, name='signup.html'
    )

@auth_router.post("/signup")
def signup(
    request: Request,
    client: Client,
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    ph_no: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    try:
        client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {
                "name": name,
                "ph_no": ph_no
            }}
        })
        
    except Exception as error:
        return error
