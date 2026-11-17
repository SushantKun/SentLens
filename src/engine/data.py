import random

USERNAMES = [
    "admin",
    "administrator",
    "root",
    "backup_admin",
    "john",
    "alice",
    "david",
    "sarah",
    "testuser",
]

EMPLOYEES = [
    "John Smith",
    "Alice Johnson",
    "David Brown",
    "Sarah Wilson",
    "Michael Lee",
]

DOMAINS = [
    "micros0ft-login.com",
    "secure-paypal.net",
    "google-authentication.net",
    "office365-login.net",
    "dropbox-share.net",
]

COMMON_PORTS = [
    20,
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    135,
    139,
    143,
    443,
    445,
    993,
    995,
    1433,
    1521,
    3306,
    3389,
    5432,
    5900,
    8080,
]


def random_username():

    return random.choice(USERNAMES)


def random_employee():

    return random.choice(EMPLOYEES)


def random_domain():

    return random.choice(DOMAINS)


def random_ip():

    return ".".join(

        str(random.randint(1, 254))

        for _ in range(4)

    )