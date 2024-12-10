from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class RagSource:
    source_id: str
    message_id: str
    document_path: str
    relevance_score: float
    created_at: datetime

@dataclass
class UploadResult:
    filename: str
    success: bool
    error: Optional[str] = None
    upload_time: datetime = datetime.now()

@dataclass
class SessionFile:
    session_id: str
    file_path: str
    created_at: datetime