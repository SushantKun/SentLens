import random

from models import LogEntry

from engine.data import random_ip, random_username


def generate():
    username = random_username()
    attacker_ip = random_ip()
    logs = []

    failed_attempts = random.randint(5, 8)

    for _ in range(failed_attempts):
        logs.append(
            LogEntry(
                timestamp="",
                source="Windows Security",
                level="Warning",
                message=(
                    "Event ID 4625 | Authentication failure | "
                    f"Account={username} | "
                    f"SourceNetworkAddress={attacker_ip}"
                ),
            )
        )

    variant = random.choice(
        ["blocked_attempt", "account_takeover"]
    )

    if variant == "blocked_attempt":
        logs.append(
            LogEntry(
                timestamp="",
                source="Identity Protection",
                level="Warning",
                message=(
                    "Adaptive access policy triggered | "
                    f"Account={username} | "
                    f"SourceNetworkAddress={attacker_ip}"
                ),
            )
        )

    else:
        logs.append(
            LogEntry(
                timestamp="",
                source="Windows Security",
                level="Information",
                message=(
                    "Event ID 4624 | Interactive logon successful | "
                    f"Account={username} | "
                    f"SourceNetworkAddress={attacker_ip}"
                ),
            )
        )

        if random.random() < 0.75:
            logs.append(
                LogEntry(
                    timestamp="",
                    source="Windows Security",
                    level="Critical",
                    message=(
                        "Event ID 4720 | New administrative account created | "
                        f"Account={random_username()}_support"
                    ),
                )
            )

    return logs