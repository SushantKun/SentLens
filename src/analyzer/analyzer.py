from analyzer.indicators import build_case_metrics, extract_indicators
from analyzer.mitre import get_mitre_info
from analyzer.rules import (
    detect_brute_force,
    detect_insider_threat,
    detect_phishing,
    detect_port_scan,
)
from analyzer.scoring import calculate_confidence


ATTACK_SEVERITIES = {
    "Brute Force Attack": "High",
    "Port Scan": "Medium",
    "Phishing Attack": "High",
    "Insider Threat": "Critical",
}


def analyze_incident(incident):
    """
    Classify an incident from event evidence only.

    incident.attack_type is hidden generator metadata and is not used
    to identify the attack.
    """

    detection_rules = {
        "Brute Force Attack": detect_brute_force,
        "Port Scan": detect_port_scan,
        "Phishing Attack": detect_phishing,
        "Insider Threat": detect_insider_threat,
    }

    candidates = []

    for attack_name, detector in detection_rules.items():
        evidence = detector(incident.logs)
        confidence = calculate_confidence(evidence, attack_name)

        candidates.append(
            {
                "attack": attack_name,
                "confidence": confidence,
                "evidence": evidence,
            }
        )

    best_match = max(
        candidates,
        key=lambda candidate: candidate["confidence"],
    )

    attack = best_match["attack"]
    confidence = best_match["confidence"]
    evidence = best_match["evidence"]

    if confidence == 0:
        attack = "Unknown"
        severity = "Unassessed"
        evidence = ["No known attack pattern was identified."]
        mitre = get_mitre_info("Unknown")
    else:
        severity = ATTACK_SEVERITIES[attack]
        mitre = get_mitre_info(attack)

    return {
        "case_id": incident.case_id,
        "attack": attack,
        "severity": severity,
        "source": incident.source,
        "confidence": confidence,
        "evidence": evidence,
        "mitre": mitre,
        "indicators": extract_indicators(incident.logs),
        "metrics": build_case_metrics(incident.logs),
    }