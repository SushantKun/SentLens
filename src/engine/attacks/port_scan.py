import random

from models import LogEntry

from engine.data import COMMON_PORTS, random_ip


def generate():
    attacker_ip = random_ip()
    target_ip = f"10.0.{random.randint(1, 20)}.{random.randint(10, 240)}"

    ports = random.sample(
        COMMON_PORTS,
        random.randint(6, 10),
    )

    logs = []

    for port in ports:
        action = random.choice(["DENY", "ALLOW"])

        logs.append(
            LogEntry(
                timestamp="",
                source="Firewall",
                level="Information",
                message=(
                    f"Firewall {action} | "
                    f"src={attacker_ip} | "
                    f"dst={target_ip} | "
                    f"protocol=TCP | dport={port}"
                ),
            )
        )

    logs.append(
        LogEntry(
            timestamp="",
            source="IDS",
            level="Warning",
            message=(
                "Network connection-rate threshold exceeded | "
                f"Source={attacker_ip} | "
                f"Target={target_ip}"
            ),
        )
    )

    if random.random() < 0.8:
        logs.append(
            LogEntry(
                timestamp="",
                source="Firewall",
                level="Critical",
                message=(
                    "Automated firewall rule applied | "
                    f"Connection blocked for source {attacker_ip}"
                ),
            )
        )

    return logs