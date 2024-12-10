from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, Optional

@dataclass
class StageFile:
    name: str
    size: int
    md5: Optional[str] = None
    last_modified: Optional[datetime] = None

    def to_dict(self) -> Dict:
        """Convert ChunkCount to dictionary"""
        return asdict(self)
