from os import getenv
from dotenv import load_dotenv
from typing import Annotated

from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, JSONResponse

from supabase import Client, create_client

load_dotenv("./config.env")

# supbase config
url = getenv("URL")
key = getenv("KEY")

s_client: Client = create_client(url, key)

auth_router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory="templates")

def get_supabase_client():
    return s_client

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

@auth_router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        request, name='login.html'
    )

@auth_router.post("/signup")
def signup(
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    ph_no: Annotated[str, Form()],
    password: Annotated[str, Form()],
    client: Client = Depends(get_supabase_client)
):
    try:
        res = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": name,
                    "ph_no": ph_no
                }
            }
        }
        )
        print(res)
        return RedirectResponse(url='/auth/login', status_code=303)

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
@auth_router.post("/login")
def login_user(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    client: Client = Depends(get_supabase_client)
):
    try:
        res = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        }).session
        token = res.access_token
        print(f"token: {token}")
        response = RedirectResponse(
            url='/dashboard', status_code=302
        )
        response.set_cookie("token", token)
        return response

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
@auth_router.post("/login_client")
def login_client(email: str, password: str, client: Client = Depends(get_supabase_client)):
    try:
        res = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        }).session
        return JSONResponse(content={
            "msg": "success",
            "name": res.user.user_metadata['name'],
            "ph_no": res.user.user_metadata['ph_no']
        })
    
    except Exception as error:
        return JSONResponse(content={"msg": "failed to login", "error": str(error)})


@auth_router.post("/verify_jwt")
def verify_jwt(jwt: str, client: Client = Depends(get_supabase_client)):
    res = client.auth.get_claims(jwt)
    return JSONResponse(content={
        'name': res['claims']['user_metadata']['name'],
        'ph_no': res['claims']['user_metadata']['ph_no']
        })

@auth_router.get("/signout")
def signout():
    res = RedirectResponse(url='/auth/login')
    res.delete_cookie("token")
    return res

