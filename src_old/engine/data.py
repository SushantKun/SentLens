import random

# -----------------------------
# Users
# -----------------------------

USERNAMES = [
    "admin",
    "administrator",
    "root",
    "john",
    "alice",
    "david",
    "mary",
    "backup",
    "finance",
    "guest"
]

# -----------------------------
# Employee Names
# -----------------------------

EMPLOYEES = [
    "John Smith",
    "Alice Brown",
    "David Wilson",
    "Emma Johnson",
    "Michael Lee",
    "Sarah Davis"
]

# -----------------------------
# Domains
# -----------------------------

PHISHING_DOMAINS = [
    "micr0soft-login.com",
    "secure-office365.net",
    "paypal-security.co",
    "google-verification.net",
    "account-security.live",
    "dropbox-login.co"
]

# -----------------------------
# Ports
# -----------------------------

COMMON_PORTS = [
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
    389,
    443,
    445,
    3389
]

# -----------------------------
# Helper Functions
# -----------------------------

def random_ip():

    return ".".join(
        str(random.randint(1, 254))
        for _ in range(4)
    )


def random_time():

    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return f"{hour:02}:{minute:02}:{second:02}"


def random_username():

    return random.choice(USERNAMES)


def random_employee():

    return random.choice(EMPLOYEES)


def random_domain():

    return random.choice(PHISHING_DOMAINS)