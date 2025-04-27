import os
import json

# Path where player progress files are stored
PROGRESS_FOLDER = "agents/npc_agent/progress"

# Ensure progress folder exists
os.makedirs(PROGRESS_FOLDER, exist_ok=True)

def get_progress_file(player_id: str) -> str:
    return os.path.join(PROGRESS_FOLDER, f"{player_id}.json")

def load_progress(player_id: str) -> dict:
    path = get_progress_file(player_id)
    if not os.path.exists(path):
        return {
            "player_id": player_id,
            "active_quests": [],
            "completed_quests": [],
            "failed_quests": [],
            "trust": {}
        }
    with open(path, "r") as f:
        return json.load(f)

def save_progress(player_id: str, progress: dict):
    path = get_progress_file(player_id)
    with open(path, "w") as f:
        json.dump(progress, f, indent=4)

def delete_progress(player_id: str):
    path = get_progress_file(player_id)
    if os.path.exists(path):
        os.remove(path)

def create_if_not_exists(player_id: str):
    path = get_progress_file(player_id)
    if not os.path.exists(path):
        save_progress(player_id, load_progress(player_id))
