import random
from datetime import datetime

from models import Incident

from engine.attack_factory import ATTACKS
from engine.background import compose_case_logs


class IncidentGenerator:
    def __init__(self):
        self.case_counter = 1

    def generate(self):
        attack_name = random.choice(list(ATTACKS.keys()))
        attack = ATTACKS[attack_name]

        attack_logs = attack["generator"]()
        case_logs = compose_case_logs(attack_logs)

        incident = Incident(
            case_id=self.case_counter,
            attack_type=attack_name,
            severity=attack["severity"],
            source=attack["source"],
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            logs=case_logs,
        )

        self.case_counter += 1

        return incident