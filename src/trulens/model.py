from dataclasses import dataclass
from typing import Optional


@dataclass
class TrulensMetric:
    value: float
    explanation: Optional[str]
    error: Optional[str]


@dataclass
class TrulensAnnotation:
    id: str  # id of the annotated entry
    groundedness: Optional[TrulensMetric] = None
    context_relevance: Optional[TrulensMetric] = None
    answer_relevance: Optional[TrulensMetric] = None