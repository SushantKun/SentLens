def get_recommendations(attack_type):
    recommendations = {
        "Brute Force Attack": [
            "Reset credentials for the affected account.",
            "Block the suspicious source IP address.",
            "Enable multi-factor authentication.",
            "Review newly created administrator accounts.",
        ],
        "Port Scan": [
            "Block or monitor the scanning source IP address.",
            "Review exposed services and unnecessary open ports.",
            "Check firewall and IDS logs for follow-up activity.",
            "Confirm critical services are patched.",
        ],
        "Phishing Attack": [
            "Isolate the affected endpoint if suspicious activity continues.",
            "Reset the affected user's credentials.",
            "Block the sender domain and related indicators.",
            "Review email gateway logs for similar messages.",
        ],
        "Insider Threat": [
            "Review the user's file-access history.",
            "Investigate external storage and data-transfer activity.",
            "Preserve relevant logs and evidence.",
            "Coordinate with security and HR before restoring access.",
        ],
    }

    return recommendations.get(
        attack_type,
        ["Review the incident evidence and continue investigation."]
    )


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

    for recommendation in get_recommendations(result["attack"]):
        lines.append(f"- {recommendation}")

    lines.append("=" * 70)

    return "\n".join(lines)