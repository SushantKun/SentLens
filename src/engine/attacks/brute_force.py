import random

from models import LogEntry

from engine.timeline import Timeline
from engine.data import (
    random_ip,
    random_username,
)


def generate():

    timeline = Timeline()
    timeline.reset()

    username = random_username()
    ip = random_ip()

    logs = []

    failed_attempts = random.randint(5, 8)

    for _ in range(failed_attempts):

        logs.append(

            LogEntry(

                timestamp=timeline.next_timestamp(),

                source="Windows Security",

                level="Warning",

                message=f"LOGIN FAILED - user: {username} - IP: {ip}"

            )

        )

    logs.append(

        LogEntry(

            timestamp=timeline.next_timestamp(),

            source="Windows Security",

            level="Information",

            message=f"LOGIN SUCCESS - user: {username} - IP: {ip}"

        )

    )

    if random.random() < 0.75:

        logs.append(

            LogEntry(

                timestamp=timeline.next_timestamp(),

                source="Windows Security",

                level="Critical",

                message=f"NEW ADMIN ACCOUNT CREATED - {random_username()}_admin"

            )

        )

    return logs