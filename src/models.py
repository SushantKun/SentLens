from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Incident:
    """
    Represents a single cyber security incident.
    """

    case_id: int
    true_attack: str
    severity: str
    logs: List[str]

    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    analyzed: bool = False