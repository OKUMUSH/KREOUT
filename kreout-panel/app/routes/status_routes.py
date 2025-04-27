from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from auth import verify_token

import subprocess
import psutil
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Refactored status route to support multiple servers
@router.get("/{server_name}", dependencies=[Depends(verify_token)])
def get_status(server_name: str):
    result = subprocess.run(f"screen -ls | grep {server_name}", shell=True, capture_output=True, text=True)
    is_running = server_name in result.stdout
    return {"server": server_name, "status": "running" if is_running else "stopped"}

@router.get("/ping", dependencies=[Depends(verify_token)])
async def ping():
    return {"message": "pong"}

@router.get("/", response_class=HTMLResponse, dependencies=[Depends(verify_token)])
async def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})   


# Route for memory and CPU usage
@router.get("/metrics", dependencies=[Depends(verify_token)])
def get_system_metrics():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory()._asdict()
    }

# Route for server logs
@router.get("/logs", dependencies=[Depends(verify_token)])
def get_logs():
    try:
        with open("/app/logs/survival.log", "r") as log_file:
            lines = log_file.readlines()[-50:]  # get last 50 lines
        return {"logs": lines}
    except FileNotFoundError:
        return {"logs": [], "error": "Log file not found"}