import random

from models import LogEntry

from engine.timeline import Timeline
from engine.data import (
    random_employee,
    random_domain,
)


def generate():

    timeline = Timeline()
    timeline.reset()

    employee = random_employee()
    domain = random_domain()

    logs = []

    email_id = random.randint(10000, 99999)

    logs.append(

        LogEntry(

            timestamp=timeline.next_timestamp(),

            source="Email Gateway",

            level="Information",

            message=(
                f"Incoming email received | "
                f"Sender domain: {domain} | "
                f"Email ID: {email_id}"
            )

        )

    )

    logs.append(

        LogEntry(

            timestamp=timeline.next_timestamp(),

            source="Email Gateway",

            level="Warning",

            message=(
                f"Suspicious attachment detected | "
                f"Target user: {employee} | "
                f"Attachment: Invoice_{random.randint(100,999)}.pdf"
            )

        )

    )

    logs.append(

        LogEntry(

            timestamp=timeline.next_timestamp(),

            source="Endpoint Security",

            level="Warning",

            message=(
                f"User {employee} opened suspicious document | "
                f"Macro execution attempt detected"
            )

        )

    )

    if random.random() < 0.8:

        logs.append(

            LogEntry(

                timestamp=timeline.next_timestamp(),

                source="Endpoint Security",

                level="Critical",

                message=(
                    f"Malicious payload blocked after execution attempt | "
                    f"User: {employee}"
                )

            )

        )

    return logs