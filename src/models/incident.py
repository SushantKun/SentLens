from dataclasses import dataclass, field
from typing import List

from models.log_entry import LogEntry


@dataclass
class Incident:
    case_id: int
    attack_type: str
    severity: str
    source: str
    created_at: str
    logs: List[LogEntry] = field(default_factory=list)