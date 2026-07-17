import random

from models.incident import Incident

from engine.templates import (
    generate_brute_force_logs,
    generate_port_scan_logs,
    generate_phishing_logs,
    generate_insider_logs
)

_case_counter = 1


def next_case_id():
    global _case_counter

    case = _case_counter
    _case_counter += 1

    return case


SCENARIOS = {

    "brute_force": {
        "severity": "High",
        "generator": generate_brute_force_logs
    },

    "port_scan": {
        "severity": "Medium",
        "generator": generate_port_scan_logs
    },

    "phishing": {
        "severity": "High",
        "generator": generate_phishing_logs
    },

    "insider_threat": {
        "severity": "Critical",
        "generator": generate_insider_logs
    }

}


def generate_scenario(name):

    scenario = SCENARIOS[name]

    return Incident(

        case_id=next_case_id(),

        true_attack=name,

        severity=scenario["severity"],

        logs=scenario["generator"]()

    )


def generate_random_scenario():

    return generate_scenario(

        random.choice(

            list(SCENARIOS.keys())

        )

    )