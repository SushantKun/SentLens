from analyzer.rules import (
    detect_brute_force,
    detect_port_scan,
    detect_phishing,
    detect_insider_threat,
)

from analyzer.mitre import get_mitre_info

from analyzer.scoring import calculate_confidence


def analyze_incident(incident):

    evidence = []

    attack = incident.attack_type


    if attack == "Brute Force Attack":

        evidence = detect_brute_force(
            incident.logs
        )


    elif attack == "Port Scan":

        evidence = detect_port_scan(
            incident.logs
        )


    elif attack == "Phishing Attack":

        evidence = detect_phishing(
            incident.logs
        )


    elif attack == "Insider Threat":

        evidence = detect_insider_threat(
            incident.logs
        )


    confidence = calculate_confidence(
        evidence,
        attack
    )


    mitre = get_mitre_info(
        attack
    )


    return {

        "case_id": incident.case_id,

        "attack": attack,

        "severity": incident.severity,

        "source": incident.source,

        "confidence": confidence,

        "evidence": evidence,

        "mitre": mitre

    }