from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class StageFile:
    name: str
    size: int
    status: str
    created_at: Optional[datetime] = None
    last_modified: Optional[datetime] = None