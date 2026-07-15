from models import Incident


def analyze_logs(incident: Incident):
    """
    Analyze an incident and return investigation results.
    """

    logs = incident.logs

    attack = "Unknown"
    confidence = 0
    evidence = []

    log_text = " ".join(logs).lower()

    # -------------------------
    # Brute Force Detection
    # -------------------------

    failed_logins = log_text.count("login failed")

    if failed_logins >= 5:
        attack = "Brute Force Attack"
        confidence = 95

        evidence.append(
            f"{failed_logins} failed login attempts detected"
        )

        if "login success" in log_text:
            evidence.append(
                "Successful login after repeated failures"
            )

        if "admin account created" in log_text:
            evidence.append(
                "Administrator account creation detected"
            )


    # -------------------------
    # Port Scan Detection
    # -------------------------

    elif "tcp syn" in log_text:

        ports = log_text.count("tcp syn")

        if ports >= 5:
            attack = "Port Scan"
            confidence = 90

            evidence.append(
                f"{ports} TCP SYN requests detected"
            )

            evidence.append(
                "Multiple ports probed in short succession"
            )


    # -------------------------
    # Phishing Detection
    # -------------------------

    elif (
        "suspicious link" in log_text
        or "credentials submitted" in log_text
    ):

        attack = "Phishing Attack"
        confidence = 92

        evidence.append(
            "Suspicious link interaction detected"
        )

        evidence.append(
            "Credential submission detected"
        )

        if "unknown ip" in log_text:
            evidence.append(
                "Login from unknown location detected"
            )


    # -------------------------
    # Insider Threat Detection
    # -------------------------

    elif (
        "usb device" in log_text
        or "removable drive" in log_text
    ):

        attack = "Insider Threat"
        confidence = 94

        evidence.append(
            "External storage device activity detected"
        )

        evidence.append(
            "Sensitive data movement detected"
        )


    else:

        evidence.append(
            "No known attack pattern detected"
        )


    incident.analyzed = True


    return {
        "attack": attack,
        "confidence": confidence,
        "reason": evidence
    }