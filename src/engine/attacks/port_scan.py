import random

from models import LogEntry

from engine.timeline import Timeline
from engine.data import (
    random_ip,
    COMMON_PORTS,
)


def generate():

    timeline = Timeline()
    timeline.reset()

    attacker_ip = random_ip()

    logs = []

    ports = random.sample(COMMON_PORTS, random.randint(6, 10))

    for port in ports:

        logs.append(

            LogEntry(

                timestamp=timeline.next_timestamp(),

                source="Firewall",

                level="Information",

                message=f"TCP SYN scan detected from {attacker_ip} on port {port}"

            )

        )

    logs.append(

        LogEntry(

            timestamp=timeline.next_timestamp(),

            source="IDS",

            level="Warning",

            message=f"Port scan threshold exceeded for {attacker_ip}"

        )

    )

    if random.random() < 0.8:

        logs.append(

            LogEntry(

                timestamp=timeline.next_timestamp(),

                source="Firewall",

                level="Critical",

                message=f"Source IP {attacker_ip} automatically blocked"

            )

        )

    return logs