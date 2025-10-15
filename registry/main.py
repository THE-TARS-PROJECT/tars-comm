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

# supbase config
url = "https://wtmxnlnqpcunnykgvmgt.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0bXhubG5xcGN1bm55a2d2bWd0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA1MDkyNDIsImV4cCI6MjA3NjA4NTI0Mn0.xjRy5qyYsrXjMa8y1B0jZHTLlKXSvi_o8qcLEeJuBdU"

s_client: Client = create_client(url, key)