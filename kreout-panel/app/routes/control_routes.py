from fastapi import APIRouter, Depends
from services.mc_control import start_server, stop_server, restart_server, send_command
from auth import verify_token

router = APIRouter()

@router.post("/{server_id}/start")
def start(server_id: str, token: str = Depends(verify_token)):
    start_server(server_id)
    return {"status": f"{server_id} started"}

@router.post("/{server_id}/stop")
def stop(server_id: str, token: str = Depends(verify_token)):
    stop_server(server_id)
    return {"status": f"{server_id} stopped"}

@router.post("/{server_id}/restart")
def restart(server_id: str, token: str = Depends(verify_token)):
    restart_server(server_id)
    return {"status": f"{server_id} restarted"}

@router.post("/{server_id}/command")
def command(server_id: str, cmd: str, token: str = Depends(verify_token)):
    send_command(server_id, cmd)
    return {"status": "command sent", "server": server_id, "command": cmd}

@router.get("/{server_id}/status")
def get_status(server_id: str, token: str = Depends(verify_token)):
    # Replace with actual status fetching logic
    return {"status": "running", "server": server_id}