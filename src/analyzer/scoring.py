def calculate_confidence(evidence, attack_type):
    score = 0

    for item in evidence:
        text = item.lower()

        if "failed login" in text:
            score += 30

        if "successful login" in text:
            score += 20

        if "administrative account" in text:
            score += 25

        if "port scanning" in text:
            score += 35

        if "connection-rate threshold" in text:
            score += 20

        if "firewall blocked" in text:
            score += 25

        if "email attachment" in text:
            score += 20

        if "untrusted url" in text:
            score += 20

        if "macro" in text or "command execution" in text:
            score += 30

        if "credential submission" in text:
            score += 30

        if "payload execution" in text:
            score += 20

        if "unusual file access" in text:
            score += 25

        if "data exfiltration" in text:
            score += 35

        if "suspended" in text:
            score += 20

    if attack_type == "Brute Force Attack" and len(evidence) >= 2:
        score += 10

    elif attack_type == "Port Scan" and len(evidence) >= 2:
        score += 10

    elif attack_type == "Phishing Attack" and len(evidence) >= 2:
        score += 10

    elif attack_type == "Insider Threat" and len(evidence) >= 2:
        score += 10

    return min(score, 100)