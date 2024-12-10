from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentChunk:
    relative_path: str
    size: int
    file_url: str
    scoped_file_url: str
    chunk: str
    category: Optional[str] = None