from datetime import datetime, timedelta
import random


class Timeline:

    def __init__(self):

        self.current_time = None

    def reset(self):

        hour = random.randint(8, 18)

        minute = random.randint(0, 59)

        second = random.randint(0, 59)

        self.current_time = datetime.strptime(
            f"{hour:02}:{minute:02}:{second:02}",
            "%H:%M:%S"
        )

    def next_timestamp(self):

        if self.current_time is None:

            self.reset()

        self.current_time += timedelta(

            seconds=random.randint(1, 5)

        )

        return self.current_time.strftime("%H:%M:%S")