import re
from collections import Counter


IP_PATTERN = re.compile(
    r"\b(?:25[0-5]|2[0-4]\d|1?\d?\d)"
    r"(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b"
)

DOMAIN_PATTERN = re.compile(
    r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b"
)

PORT_PATTERN = re.compile(
    r"(?:dport=|port\s)(\d{1,5})",
    re.IGNORECASE,
)

USER_PATTERN = re.compile(
    r"(?:user|employee|account)\s*:\s*([^|]+)",
    re.IGNORECASE,
)

FILE_PATTERN = re.compile(
    r"(?:attachment|file)\s*:\s*([^|]+)",
    re.IGNORECASE,
)

SUSPICIOUS_KEYWORDS = (
    "failed",
    "scan",
    "suspicious",
    "macro",
    "malicious",
    "blocked",
    "untrusted",
    "credential",
    "unusual",
    "bulk",
    "external",
    "removable",
    "data transfer",
    "account created",
    "suspended",
    "detected",
)


def unique_values(values):
    return list(dict.fromkeys(value.strip() for value in values if value.strip()))


def extract_indicators(logs):
    ips = []
    domains = []
    ports = []
    users = []
    files = []

    for log in logs:
        message = log.message

        ips.extend(IP_PATTERN.findall(message))
        domains.extend(DOMAIN_PATTERN.findall(message))
        ports.extend(PORT_PATTERN.findall(message))

        user_match = USER_PATTERN.search(message)
        if user_match:
            users.append(user_match.group(1).strip())

        file_match = FILE_PATTERN.search(message)
        if file_match:
            files.append(file_match.group(1).strip())

    return {
        "ips": unique_values(ips),
        "domains": unique_values(domains),
        "ports": unique_values(ports),
        "users": unique_values(users),
        "files": unique_values(files),
    }


def build_case_metrics(logs):
    source_counts = Counter(log.source for log in logs)
    level_counts = Counter(log.level for log in logs)

    suspicious_events = 0

    for log in logs:
        message = log.message.lower()

        if any(keyword in message for keyword in SUSPICIOUS_KEYWORDS):
            suspicious_events += 1

    return {
        "total_events": len(logs),
        "suspicious_events": suspicious_events,
        "normal_events": max(0, len(logs) - suspicious_events),
        "critical_events": level_counts.get("Critical", 0),
        "warning_events": level_counts.get("Warning", 0),
        "information_events": level_counts.get("Information", 0),
        "source_count": len(source_counts),
        "first_timestamp": logs[0].timestamp if logs else "--",
        "last_timestamp": logs[-1].timestamp if logs else "--",
        "source_counts": dict(source_counts),
        "level_counts": dict(level_counts),
    }