from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

import os
import json

router = APIRouter()

BASE_NPCS_FOLDER = "agents/npc_agent/npcs"

def save_json_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@router.post("/create")
async def create_npc(request: Request):
    data = await request.json()

    npc_id = data.get("id")
    npc_name = data.get("name")
    personality = data.get("personality")
    interests = data.get("interests", [])

    if not npc_id or not npc_name:
        raise HTTPException(status_code=400, detail="NPC id and name are required.")

    npc_folder = os.path.join(BASE_NPCS_FOLDER, npc_id)

    if os.path.exists(npc_folder):
        raise HTTPException(status_code=400, detail="NPC already exists!")

    os.makedirs(npc_folder, exist_ok=True)

    # Save all NPC-related JSON files
    save_json_file(os.path.join(npc_folder, "npc.json"), {
        "id": npc_id,
        "name": npc_name,
        "background": "An enigmatic figure with a rich backstory yet to be unveiled.",
        "personality": personality,
        "interests": interests,
        "dialog": {
            "default": "Greetings, traveler. What brings you to these lands?",
            "trust_levels": [
                {"min_trust": 0, "text": "I don't deal with strangers. Earn my trust first."},
                {"min_trust": 40, "text": "You're starting to prove yourself. Let's see where this goes."},
                {"min_trust": 50, "text": "You've earned my respect. I have secrets and rewards for those I trust deeply."}
            ],
            "shop_unlocked": "The best goods are reserved for trusted friends."
        },
        "files": {
            "main_quests_file": "quests.json",
            "side_quests_file": "side_quests.json",
            "shop_file": "shop.json",
            "special_shop_file": "special_shop.json",
            "trust_file": "trust.json",
            "achievements_file": "achievements.json"
        }
    })

    save_json_file(os.path.join(npc_folder, "quests.json"), {"quests": []})
    save_json_file(os.path.join(npc_folder, "side_quests.json"), {"quests": []})
    save_json_file(os.path.join(npc_folder, "shop.json"), {"items_for_sale": []})
    save_json_file(os.path.join(npc_folder, "trust.json"), {"trust_rewards": {}})
    save_json_file(os.path.join(npc_folder, "achievements.json"), {"achievements": []})

    return JSONResponse(content={"message": f"NPC '{npc_name}' created successfully!"})