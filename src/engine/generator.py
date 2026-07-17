import random
from datetime import datetime

from models import Incident

from engine.attack_factory import ATTACKS


class IncidentGenerator:

    def __init__(self):

        self.case_counter = 1

    def generate(self):

        attack_name = random.choice(

            list(ATTACKS.keys())

        )

        attack = ATTACKS[attack_name]

        logs = attack["generator"]()

        incident = Incident(

            case_id=self.case_counter,

            attack_type=attack_name,

            severity=attack["severity"],

            source=attack["source"],

            created_at=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            logs=logs

        )

        self.case_counter += 1

        return incident