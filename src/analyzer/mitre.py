UNKNOWN_TECHNIQUE = {
    "id": "Unknown",
    "name": "No ATT&CK mapping",
    "description": "No supported ATT&CK technique was identified.",
}


def get_mitre_techniques(attack_type, logs):
    messages = " ".join(
        log.message.lower()
        for log in logs
    )

    if attack_type == "Brute Force Attack":
        techniques = [
            {
                "id": "T1110",
                "name": "Brute Force",
                "description": (
                    "Repeated authentication attempts were detected."
                ),
            }
        ]

        if "login success" in messages or "event id 4624" in messages:
            techniques.append(
                {
                    "id": "T1078",
                    "name": "Valid Accounts",
                    "description": (
                        "A successful sign-in followed repeated failures."
                    ),
                }
            )

        if "admin account created" in messages or "event id 4720" in messages:
            techniques.append(
                {
                    "id": "T1136",
                    "name": "Create Account",
                    "description": (
                        "A new account was created after authentication activity."
                    ),
                }
            )

        return techniques

    if attack_type == "Port Scan":
        return [
            {
                "id": "T1046",
                "name": "Network Service Discovery",
                "description": (
                    "Sequential service and port probing was detected."
                ),
            }
        ]

    if attack_type == "Phishing Attack":
        techniques = []

        if "attachment" in messages:
            techniques.append(
                {
                    "id": "T1566.001",
                    "name": "Phishing: Spearphishing Attachment",
                    "description": (
                        "A suspicious email attachment was delivered."
                    ),
                }
            )

        if "untrusted" in messages or "credentials submitted" in messages:
            techniques.append(
                {
                    "id": "T1566.002",
                    "name": "Phishing: Spearphishing Link",
                    "description": (
                        "A suspicious link or credential-harvesting activity "
                        "was observed."
                    ),
                }
            )

        if "opened suspicious document" in messages or "macro execution" in messages:
            techniques.append(
                {
                    "id": "T1204.002",
                    "name": "User Execution: Malicious File",
                    "description": (
                        "A user opened a suspicious file or initiated macro activity."
                    ),
                }
            )

        return techniques or [UNKNOWN_TECHNIQUE]

    if attack_type == "Insider Threat":
        techniques = [
            {
                "id": "T1078",
                "name": "Valid Accounts",
                "description": (
                    "A legitimate authenticated account accessed sensitive resources."
                ),
            }
        ]

        if "external storage" in messages or "data transfer" in messages:
            techniques.append(
                {
                    "id": "T1567.002",
                    "name": "Exfiltration Over Web Service: Cloud Storage",
                    "description": (
                        "Potential transfer of data to external storage was observed."
                    ),
                }
            )

        return techniques

    return [UNKNOWN_TECHNIQUE]


def get_mitre_info(attack_type):
    return get_mitre_techniques(attack_type, [])[0]