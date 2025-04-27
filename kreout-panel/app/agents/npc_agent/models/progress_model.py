from pydantic import BaseModel
from typing import Dict, List, Optional

class QuestProgress(BaseModel):
    completed: List[str] = []
    active: List[str] = []
    failed: List[str] = []

class NPCProgress(BaseModel):
    trust: int = 0
    quests: QuestProgress = QuestProgress()
    shop_unlocked: bool = False
    special_shop_unlocked: bool = False

class PlayerProgress(BaseModel):
    player_id: str
    npcs: Dict[str, NPCProgress] = {}
