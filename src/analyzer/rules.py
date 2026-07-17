def _messages(logs):
    return [log.message.lower() for log in logs]


def detect_brute_force(logs):
    evidence = []
    messages = _messages(logs)

    failed_attempts = sum(
        "event id 4625" in message or "login failed" in message
        for message in messages
    )

    successful_login = any(
        "event id 4624" in message or "login success" in message
        for message in messages
    )

    admin_created = any(
        "event id 4720" in message or "admin account created" in message
        for message in messages
    )

    if failed_attempts >= 5:
        evidence.append(
            f"Detected {failed_attempts} failed login attempts"
        )

    if successful_login:
        evidence.append(
            "Successful login occurred after repeated failures"
        )

    if admin_created:
        evidence.append(
            "New administrative account creation detected"
        )

    return evidence


def detect_port_scan(logs):
    evidence = []
    messages = _messages(logs)

    probe_count = sum(
        "dport=" in message or "tcp syn scan" in message
        for message in messages
    )

    threshold_exceeded = any(
        "threshold exceeded" in message
        or "connection-rate threshold" in message
        for message in messages
    )

    blocked = any(
        "rule applied" in message
        or "automatically blocked" in message
        or "connection blocked" in message
        for message in messages
    )

    if probe_count >= 5:
        evidence.append(
            f"Multiple port scanning attempts detected ({probe_count} connection attempts)"
        )

    if threshold_exceeded:
        evidence.append(
            "Network connection-rate threshold exceeded"
        )

    if blocked:
        evidence.append(
            "Firewall blocked suspicious source"
        )

    return evidence


def detect_phishing(logs):
    evidence = []
    messages = _messages(logs)

    attachment = any(
        "attachment=" in message
        or ".docm" in message
        or "suspicious attachment" in message
        for message in messages
    )

    suspicious_url = any(
        "untrusted domain" in message
        or "web gateway request" in message
        or "suspicious link" in message
        for message in messages
    )

    macro_attempt = any(
        "macro" in message
        or "command interpreter" in message
        for message in messages
    )

    credentials_submitted = any(
        "credentials submitted" in message
        or "submitted credentials" in message
        for message in messages
    )

    payload_blocked = any(
        "blocked execution" in message
        or "payload blocked" in message
        for message in messages
    )

    if attachment:
        evidence.append(
            "Suspicious email attachment detected"
        )

    if suspicious_url:
        evidence.append(
            "User interaction with an untrusted URL detected"
        )

    if macro_attempt:
        evidence.append(
            "Office macro or command execution attempt detected"
        )

    if credentials_submitted:
        evidence.append(
            "Credential submission to an untrusted service detected"
        )

    if payload_blocked:
        evidence.append(
            "Endpoint security blocked malicious payload execution"
        )

    return evidence


def detect_insider_threat(logs):
    evidence = []
    messages = _messages(logs)

    unusual_access = any(
        "bulk file read" in message
        or "unusual file access" in message
        for message in messages
    )

    external_transfer = any(
        "outbound transfer" in message
        or "external storage" in message
        or "removable media" in message
        for message in messages
    )

    account_suspended = any(
        "account temporarily suspended" in message
        or "access suspended" in message
        for message in messages
    )

    if unusual_access:
        evidence.append(
            "Unusual file access behavior detected"
        )

    if external_transfer:
        evidence.append(
            "Potential data exfiltration activity detected"
        )

    if account_suspended:
        evidence.append(
            "User account was suspended by security"
        )

    return evidence