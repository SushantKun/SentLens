import random

from engine.data import (
    random_ip,
    random_time,
    random_username,
    random_employee,
    random_domain,
    COMMON_PORTS
)

# -------------------------------------------------
# Brute Force
# -------------------------------------------------

def generate_brute_force_logs():

    username = random_username()
    ip = random_ip()

    logs = []

    failed_attempts = random.randint(5, 8)

    for _ in range(failed_attempts):
        logs.append(
            f"{random_time()} LOGIN FAILED - user: {username} - IP: {ip}"
        )

    logs.append(
        f"{random_time()} LOGIN SUCCESS - user: {username} - IP: {ip}"
    )

    if random.random() < 0.7:
        logs.append(
            f"{random_time()} NEW ADMIN ACCOUNT CREATED - {random_username()}_admin"
        )

    return logs


# -------------------------------------------------
# Port Scan
# -------------------------------------------------

def generate_port_scan_logs():

    ip = random_ip()

    ports = random.sample(COMMON_PORTS, random.randint(5, 8))

    logs = []

    for port in ports:
        logs.append(
            f"{random_time()} TCP SYN from {ip} to port {port}"
        )

    return logs


# -------------------------------------------------
# Phishing
# -------------------------------------------------

def generate_phishing_logs():

    employee = random_employee()
    domain = random_domain()
    ip = random_ip()

    return [

        f"{random_time()} Email received by {employee} from support@{domain}",

        f"{random_time()} User clicked suspicious link",

        f"{random_time()} Credentials submitted",

        f"{random_time()} Login from unknown IP {ip}"

    ]


# -------------------------------------------------
# Insider Threat
# -------------------------------------------------

def generate_insider_logs():

    employee = random_employee()

    return [

        f"{random_time()} {employee} accessed HR database",

        f"{random_time()} Exported confidential records",

        f"{random_time()} USB device connected",

        f"{random_time()} Large file copied to removable drive"

    ]