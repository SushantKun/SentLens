def get_recommendations(attack_type):
    recommendations = {
        "Brute Force Attack": [
            "Reset credentials for the affected account.",
            "Revoke active sessions and review recent sign-in activity.",
            "Block or restrict the suspicious source IP address.",
            "Enable multi-factor authentication for the affected account.",
            "Review newly created privileged accounts and access changes.",
        ],
        "Port Scan": [
            "Block or monitor the scanning source IP address.",
            "Review exposed services and close unnecessary open ports.",
            "Confirm exposed services are patched and securely configured.",
            "Review IDS and firewall logs for follow-up access attempts.",
            "Apply rate-limiting or detection rules for repeated probes.",
        ],
        "Phishing Attack": [
            "Quarantine matching emails across affected mailboxes.",
            "Reset affected credentials and revoke active sessions.",
            "Block the sender domain, malicious URL, and attachment hash.",
            "Search endpoints for related files or execution activity.",
            "Review email gateway logs for additional recipients.",
        ],
        "Insider Threat": [
            "Preserve relevant logs, file-access records, and evidence.",
            "Temporarily restrict access using least-privilege controls.",
            "Review external-storage and data-transfer activity.",
            "Investigate the user's recent file-access history.",
            "Coordinate with security and HR before restoring access.",
        ],
    }

    actions = recommendations.get(
        attack_type,
        ["Review the available evidence and continue investigation."]
    )

    actions.append(
        "Document the incident, assign an owner, and monitor for recurrence."
    )

    return actions


def format_incident_report(incident, result):
    lines = [
        "=" * 70,
        "SENTLENS INCIDENT REPORT",
        "=" * 70,
        f"CASE ID    : {result['case_id']:04d}",
        f"ATTACK     : {result['attack']}",
        f"SEVERITY   : {result['severity']}",
        f"SOURCE     : {result['source']}",
        f"CREATED AT : {incident.created_at}",
        f"CONFIDENCE : {result['confidence']}%",
        "",
        "EVIDENCE",
        "-" * 70,
    ]

    for index, item in enumerate(result["evidence"], start=1):
        lines.append(f"{index}. {item}")

    lines.extend([
        "",
        "MITRE ATT&CK",
        "-" * 70,
        f"{result['mitre']['id']} - {result['mitre']['name']}",
        result["mitre"]["description"],
        "",
        "RECOMMENDED ACTIONS",
        "-" * 70,
    ])

    for index, recommendation in enumerate(
        get_recommendations(result["attack"]),
        start=1,
    ):
        lines.append(f"{index}. {recommendation}")

    lines.append("=" * 70)

    return "\n".join(lines)