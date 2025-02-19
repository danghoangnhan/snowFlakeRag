from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Entity:
    id: str
    corpus_id: str
    type: str
    community_id: Optional[int] = None

@dataclass
class Relation:
    src_node_id: str
    dst_node_id: str
    corpus_id: str
    type: str