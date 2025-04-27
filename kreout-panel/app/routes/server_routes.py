from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
from auth import verify_token

router = APIRouter(prefix="/servers", tags=["Servers"])

# Sample database (in-memory for now)
servers_db = {}

# Request models
class ServerCreate(BaseModel):
    name: str
    host: str
    port: int
    rcon_port: Optional[int]
    max_players: Optional[int] = 100

class ServerUpdateMetrics(BaseModel):
    tps: float
    ram_usage: int  # in MB
    players_online: int

# Routes
@router.get("/", summary="List all registered servers")
def list_servers(token: str = Depends(verify_token)):
    return list(servers_db.values())

@router.post("/", summary="Register a new server")
def register_server(server: ServerCreate, token: str = Depends(verify_token)):
    if server.name in servers_db:
        raise HTTPException(status_code=400, detail="Server already exists")
    servers_db[server.name] = server.dict()
    return {"message": "Server registered successfully"}

@router.get("/{server_name}", summary="Get details for a single server")
def get_server(server_name: str, token: str = Depends(verify_token)):
    server = servers_db.get(server_name)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@router.post("/{server_name}/update", summary="Update server metrics")
def update_server_metrics(server_name: str, metrics: ServerUpdateMetrics, token: str = Depends(verify_token)):
    server = servers_db.get(server_name)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    server.update(metrics.dict())
    return {"message": "Metrics updated", "server": server}

@router.post("/{server_name}/command", summary="Send command to server")
def send_command_to_server(server_name: str, cmd: str = Query(...), token: str = Depends(verify_token)):
    server = servers_db.get(server_name)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    # Here you would integrate with RCON or socat command system
    return {"message": f"Command '{cmd}' sent to {server_name}"}