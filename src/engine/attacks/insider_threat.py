import random

from models import LogEntry

from engine.timeline import Timeline
from engine.data import (
    random_employee,
    random_ip,
)


def generate():

    timeline = Timeline()
    timeline.reset()

    employee = random_employee()
    ip = random_ip()

    logs = []

    files_accessed = random.randint(50, 300)

    logs.append(

        LogEntry(

            timestamp=timeline.next_timestamp(),

            source="Active Directory",

            level="Information",

            message=(
                f"User authentication successful | "
                f"Employee: {employee} | "
                f"Source IP: {ip}"
            )

        )

    )

    logs.append(

        LogEntry(

            timestamp=timeline.next_timestamp(),

            source="File Server",

            level="Warning",

            message=(
                f"Unusual file access pattern detected | "
                f"User: {employee} | "
                f"Files accessed: {files_accessed}"
            )

        )

    )

    logs.append(

        LogEntry(

            timestamp=timeline.next_timestamp(),

            source="Data Loss Prevention",

            level="Warning",

            message=(
                f"Large data transfer initiated by {employee} | "
                f"Destination: External Storage"
            )

        )

    )

    if random.random() < 0.85:

        logs.append(

            LogEntry(

                timestamp=timeline.next_timestamp(),

                source="Security Operations",

                level="Critical",

                message=(
                    f"Potential insider threat detected | "
                    f"Account temporarily suspended | "
                    f"User: {employee}"
                )

            )

        )

    return logs