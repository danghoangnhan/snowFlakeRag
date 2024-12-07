
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ChatSession:
    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    is_active: bool