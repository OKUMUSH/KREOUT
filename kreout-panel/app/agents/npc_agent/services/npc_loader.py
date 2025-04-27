# app/npc_agent/services/npc_loader.py

import os
import json
from pathlib import Path

NPC_DATA_PATH = Path(__file__).parent.parent / "npc_data"


def load_all_npcs():
    """Loads all NPC JSON files into a dictionary."""
    npcs = []
    for file in os.listdir(NPC_DATA_PATH):
        if file.endswith(".json"):
            path = NPC_DATA_PATH / file
            with open(path, "r", encoding="utf-8") as f:
                try:
                    npc_data = json.load(f)
                    npcs.append(npc_data)
                except Exception as e:
                    print(f"Error loading {file}: {e}")
    return npcs


def load_npc_by_id(npc_id):
    """Loads a specific NPC by ID (matching filename)."""
    file_path = NPC_DATA_PATH / f"{npc_id}.json"
    print(f"Loading NPC from: {file_path}")
    if not file_path.exists():
        raise FileNotFoundError(f"NPC file '{npc_id}.json' not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(f"Loaded NPC Data: {data}")
        return data
    
def load_npc_with_quests(npc_id):
    """Loads an NPC and also its linked quests if available."""
    npc = load_npc_by_id(npc_id)

    quests_info = npc.get("quests_linked")
    if quests_info:
        quests_file = quests_info.get("main_quests_file")
        if quests_file:
            quests_path = NPC_DATA_PATH / "quests" / quests_file
            if quests_path.exists():
                with open(quests_path, "r", encoding="utf-8") as f:
                    try:
                        quests_data = json.load(f)
                        npc["loaded_quests"] = quests_data.get("quests", [])
                    except Exception as e:
                        print(f"Error loading quests for {npc_id}: {e}")
            else:
                print(f"Warning: Quests file {quests_file} not found for {npc_id}.")

    return npc

QUESTS_FOLDER = "agents/npc_agent/quests"

def load_quests_file(filename: str):
    filepath = os.path.join(QUESTS_FOLDER, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data