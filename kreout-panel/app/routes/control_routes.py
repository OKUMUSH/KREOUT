from fastapi import APIRouter
from services.mc_control import start_server, stop_server, restart_server, send_command


router = APIRouter()

@router.post("/start")
def start():
    start_server()
    return {"status": "started"}

@router.post("/stop")
def stop():
    stop_server()
    return {"status": "stopped"}

@router.post("/restart")
def restart():
    restart_server()
    return {"status": "restarted"}

@router.post("/command")
def command(cmd: str):
    send_command(cmd)
    return {"status": "command sent", "command": cmd}
