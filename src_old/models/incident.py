from dataclasses import dataclass


@dataclass
class Incident:

    case_id: int

    true_attack: str

    severity: str

    logs: list