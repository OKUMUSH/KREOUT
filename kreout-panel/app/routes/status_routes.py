from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import subprocess

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/status")
def get_status():
    result = subprocess.run("screen -ls | grep survival", shell=True, capture_output=True, text=True)
    is_running = "survival" in result.stdout
    return {"server": "running" if is_running else "stopped"}
@router.get("/ping")
async def ping():
    return {"message": "pong"}

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})   