import random

from models import LogEntry

from engine.data import random_domain, random_employee, random_ip


def generate():
    employee = random_employee()
    domain = random_domain()
    logs = []

    variant = random.choice(
        ["malicious_attachment", "credential_harvest"]
    )

    if variant == "malicious_attachment":
        attachment = (
            f"Invoice_{random.randint(1000, 9999)}.docm"
        )

        logs.extend(
            [
                LogEntry(
                    timestamp="",
                    source="Email Gateway",
                    level="Information",
                    message=(
                        "Email delivered | "
                        f"sender=notifications@{domain} | "
                        f"recipient={employee} | "
                        f"attachment={attachment}"
                    ),
                ),
                LogEntry(
                    timestamp="",
                    source="Endpoint Security",
                    level="Warning",
                    message=(
                        f"Office application opened {attachment} | "
                        f"User={employee}"
                    ),
                ),
                LogEntry(
                    timestamp="",
                    source="Endpoint Security",
                    level="Warning",
                    message=(
                        "Office macro execution attempt detected | "
                        f"User={employee}"
                    ),
                ),
            ]
        )

        if random.random() < 0.8:
            logs.append(
                LogEntry(
                    timestamp="",
                    source="Endpoint Security",
                    level="Critical",
                    message=(
                        "Endpoint policy blocked execution | "
                        f"User={employee}"
                    ),
                )
            )

    else:
        fake_ip = random_ip()

        logs.extend(
            [
                LogEntry(
                    timestamp="",
                    source="Email Gateway",
                    level="Information",
                    message=(
                        "Email delivered | "
                        f"sender=account-security@{domain} | "
                        f"recipient={employee}"
                    ),
                ),
                LogEntry(
                    timestamp="",
                    source="Secure Web Gateway",
                    level="Warning",
                    message=(
                        "Web gateway request to untrusted domain | "
                        f"User={employee} | "
                        f"Domain={domain}"
                    ),
                ),
                LogEntry(
                    timestamp="",
                    source="Identity Protection",
                    level="Critical",
                    message=(
                        "User submitted credentials to untrusted service | "
                        f"Account={employee}"
                    ),
                ),
                LogEntry(
                    timestamp="",
                    source="Identity Protection",
                    level="Warning",
                    message=(
                        "Authentication request from unfamiliar address | "
                        f"Account={employee} | "
                        f"SourceNetworkAddress={fake_ip}"
                    ),
                ),
            ]
        )

    return logs