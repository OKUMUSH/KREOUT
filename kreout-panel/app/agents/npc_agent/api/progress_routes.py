from fastapi import APIRouter, HTTPException
from agents.npc_agent.services.progress_service import (
    load_progress,
    save_progress,
    delete_progress,
)

router = APIRouter(prefix="/progress", tags=["Player Progress"])

@router.get("/{player_id}")
async def get_player_progress(player_id: str):
    try:
        progress = load_progress(player_id)
        return {"player_id": player_id, "progress": progress}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{player_id}")
async def post_player_progress(player_id: str, progress: dict):
    try:
        save_progress(player_id, progress)
        return {"status": "saved", "player_id": player_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{player_id}")
async def delete_progress(player_id: str):
    try:
        delete_progress(player_id)
        return {"status": "deleted", "player_id": player_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
