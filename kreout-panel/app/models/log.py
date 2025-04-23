from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class LogEntry(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    action: str
    result: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
