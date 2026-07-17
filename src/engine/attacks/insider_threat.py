import random

from models import LogEntry

from engine.data import random_employee, random_ip


def generate():
    employee = random_employee()
    source_ip = random_ip()
    logs = []

    variant = random.choice(
        ["external_transfer", "removable_media"]
    )

    logs.extend(
        [
            LogEntry(
                timestamp="",
                source="Active Directory",
                level="Information",
                message=(
                    "Interactive logon successful | "
                    f"User={employee} | "
                    f"SourceNetworkAddress={source_ip}"
                ),
            ),
            LogEntry(
                timestamp="",
                source="File Server",
                level="Warning",
                message=(
                    "Bulk file read operation detected | "
                    f"User={employee} | "
                    f"FilesRead={random.randint(80, 300)}"
                ),
            ),
        ]
    )

    if variant == "external_transfer":
        logs.append(
            LogEntry(
                timestamp="",
                source="Data Loss Prevention",
                level="Warning",
                message=(
                    "DLP policy triggered for outbound transfer | "
                    f"User={employee} | "
                    "Destination=ExternalStorage"
                ),
            )
        )

    else:
        logs.append(
            LogEntry(
                timestamp="",
                source="Endpoint Security",
                level="Warning",
                message=(
                    "Removable media mounted after bulk file access | "
                    f"User={employee}"
                ),
            )
        )

    if random.random() < 0.85:
        logs.append(
            LogEntry(
                timestamp="",
                source="Security Operations",
                level="Critical",
                message=(
                    "Account temporarily suspended pending review | "
                    f"User={employee}"
                ),
            )
        )

    return logs