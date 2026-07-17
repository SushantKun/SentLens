import random

from models import LogEntry

from engine.data import (
    COMMON_PORTS,
    random_domain,
    random_employee,
    random_ip,
    random_username,
)
from engine.timeline import Timeline


def generate_background_events():
    """
    Create normal business and infrastructure events.
    These do not represent malicious activity.
    """

    event_count = random.randint(4, 7)
    events = []

    for _ in range(event_count):
        event_type = random.choice(
            [
                "user_login",
                "file_access",
                "backup",
                "dns_lookup",
                "firewall_allow",
                "email_delivery",
            ]
        )

        if event_type == "user_login":
            events.append(
                LogEntry(
                    timestamp="",
                    source="Active Directory",
                    level="Information",
                    message=(
                        f"Interactive logon successful | "
                        f"User: {random_username()} | "
                        f"Workstation: WS-{random.randint(100, 999)}"
                    ),
                )
            )

        elif event_type == "file_access":
            events.append(
                LogEntry(
                    timestamp="",
                    source="File Server",
                    level="Information",
                    message=(
                        f"Routine file read completed | "
                        f"User: {random_employee()} | "
                        f"Share: Department_Documents"
                    ),
                )
            )

        elif event_type == "backup":
            events.append(
                LogEntry(
                    timestamp="",
                    source="Backup Service",
                    level="Information",
                    message=(
                        f"Scheduled backup completed | "
                        f"Archive: daily_backup_{random.randint(100, 999)}.zip"
                    ),
                )
            )

        elif event_type == "dns_lookup":
            events.append(
                LogEntry(
                    timestamp="",
                    source="DNS Server",
                    level="Information",
                    message=(
                        f"DNS lookup completed | "
                        f"Host: {random_domain()}"
                    ),
                )
            )

        elif event_type == "firewall_allow":
            events.append(
                LogEntry(
                    timestamp="",
                    source="Firewall",
                    level="Information",
                    message=(
                        f"Outbound TCP session allowed | "
                        f"Source: 10.0.{random.randint(1, 50)}."
                        f"{random.randint(2, 254)} | "
                        f"Destination: {random_ip()} | "
                        f"Port: {random.choice(COMMON_PORTS)}"
                    ),
                )
            )

        elif event_type == "email_delivery":
            events.append(
                LogEntry(
                    timestamp="",
                    source="Email Gateway",
                    level="Information",
                    message=(
                        f"Internal email delivered successfully | "
                        f"Recipient: {random_employee()}"
                    ),
                )
            )

    return events


def compose_case_logs(attack_logs):
    """
    Mix normal events into attack evidence and assign one
    chronological timeline to the final incident.
    """

    background_logs = generate_background_events()
    combined_logs = list(attack_logs)

    for background_log in background_logs:
        insert_at = random.randint(0, len(combined_logs))
        combined_logs.insert(insert_at, background_log)

    timeline = Timeline()
    timeline.reset()

    for log in combined_logs:
        log.timestamp = timeline.next_timestamp()

    return combined_logs