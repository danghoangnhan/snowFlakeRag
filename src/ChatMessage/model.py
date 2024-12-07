from datetime import datetime
from dataclasses import dataclass

@dataclass
class ChatMessage:
    message_id: str
    session_id: str
    role: str
    content: str
    created_at: datetime
