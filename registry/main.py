from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth_router import auth_router

from supabase import create_client, Client

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), "static")

templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)
