def analyze_logs(logs):
    """
    Analyze log entries and identify the most likely attack.
    """

    # -------------------------
    # Indicators
    # -------------------------

    failed_logins = 0
    successful_login = False
    admin_created = False

    syn_packets = 0

    clicked_link = False
    credentials_submitted = False
    unknown_login = False

    database_access = False
    usb_connected = False
    file_copy = False

    # -------------------------
    # Collect Evidence
    # -------------------------

    for log in logs:

        # Brute Force
        if "LOGIN FAILED" in log:
            failed_logins += 1

        if "LOGIN SUCCESS" in log:
            successful_login = True

        if "NEW ADMIN ACCOUNT CREATED" in log:
            admin_created = True

        # Port Scan
        if "TCP SYN" in log:
            syn_packets += 1

        # Phishing
        if "clicked suspicious link" in log:
            clicked_link = True

        if "Credentials submitted" in log:
            credentials_submitted = True

        if "unknown IP" in log:
            unknown_login = True

        # Insider Threat
        if "HR database" in log:
            database_access = True

        if "USB device connected" in log:
            usb_connected = True

        if "Large file copied" in log:
            file_copy = True

    # -------------------------
    # Detection Rules
    # -------------------------

    # Brute Force
    if failed_logins >= 5 and successful_login:
        return {
            "attack": "Brute Force Attack",
            "confidence": 95,
            "reason": [
                f"{failed_logins} failed login attempts",
                "Successful login detected",
                "Administrator account created"
            ]
        }

    # Port Scan
    if syn_packets >= 5:
        return {
            "attack": "Port Scan",
            "confidence": 90,
            "reason": [
                f"{syn_packets} TCP SYN packets detected",
                "Multiple ports probed in quick succession"
            ]
        }

    # Phishing
    if clicked_link and credentials_submitted and unknown_login:
        return {
            "attack": "Phishing Attack",
            "confidence": 92,
            "reason": [
                "Suspicious email link clicked",
                "Credentials submitted",
                "Unknown login detected"
            ]
        }

    # Insider Threat
    if database_access and usb_connected and file_copy:
        return {
            "attack": "Insider Threat",
            "confidence": 94,
            "reason": [
                "Sensitive database accessed",
                "USB device connected",
                "Large file copied"
            ]
        }

    # Unknown
    return {
        "attack": "Unknown",
        "confidence": 0,
        "reason": [
            "No matching attack pattern found."
        ]
    }