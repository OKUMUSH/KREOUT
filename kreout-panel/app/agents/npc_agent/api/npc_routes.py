from fastapi import APIRouter, HTTPException
from agents.npc_agent.services.npc_loader import load_all_npcs, load_npc_with_quests,load_npc_by_id, load_quests_file

router = APIRouter()

@router.get("/")
def get_all_npcs():
    try:
        npcs = load_all_npcs()
        return {"npcs": npcs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{npc_id}")
def get_npc(npc_id: str):
    try:
        npc = load_npc_by_id(npc_id)
        return {"npc": npc}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="NPC not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# New route to get quests linked to an NPC
@router.get("/quests/{npc_id}")
def get_npc_quests(npc_id: str):
    try:
        npc = load_npc_with_quests(npc_id)
        quests_linked = npc.get("quests_linked", {})

        if not quests_linked:
            return {"quests": []}

        main_quests_file = quests_linked.get("main_quests_file")
        if not main_quests_file:
            return {"quests": []}

        quests = load_quests_file(main_quests_file)
        return {"quests": quests}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="NPC or quests file not found "+ main_quests_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))