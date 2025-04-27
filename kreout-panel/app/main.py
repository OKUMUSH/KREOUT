from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routes import status_routes, control_routes, server_routes as all_routes
from agents.npc_agent.api.npc_routes import router as npc_routes
from agents.npc_agent.api.progress_routes import router as progress_routes 
from agents.npc_agent.api.npc_admin_routes import router as npc_admin_routes

import os
import json

app = FastAPI()

app.include_router(status_routes, prefix="/status")
app.include_router(control_routes, prefix="/control")
app.include_router(all_routes, prefix="/servers")
app.include_router(npc_routes, prefix="/npcs")
app.include_router(progress_routes, prefix="/progress")
app.include_router(npc_admin_routes, prefix="/npcs/admin")

templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


NPC_FOLDER = "agents/npc_agent/npc_data"

templates = Jinja2Templates(directory="agents/npc_agent/templates")
@app.get("/dashboard", response_class=HTMLResponse)
async def npc_dashboard(request: Request):
    npcs = []

    for filename in os.listdir(NPC_FOLDER):
        if filename.endswith(".json"):
            with open(os.path.join(NPC_FOLDER, filename), "r", encoding="utf-8") as f:
                npc_data = json.load(f)
                npcs.append({
                    "id": npc_data.get("id", filename.replace(".json", "")),
                    "name": npc_data.get("name", "Unnamed NPC"),
                    "personality": npc_data.get("personality", "Unknown"),
                    "interests": npc_data.get("interests", []),
                    "quests_linked": npc_data.get("quests_linked", {})
                })

    return templates.TemplateResponse("npc_dashboard.html", {
        "request": request,
        "npcs": npcs
    })