def detect_brute_force(logs):

    evidence = []

    failed_attempts = 0
    successful_login = False
    admin_created = False

    for log in logs:

        message = log.message.lower()

        if "login failed" in message:
            failed_attempts += 1

        if "login success" in message:
            successful_login = True

        if "admin account created" in message:
            admin_created = True


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

    scan_events = 0
    blocked = False

    for log in logs:

        message = log.message.lower()

        if "scan detected" in message:

            scan_events += 1


        if "blocked" in message:

            blocked = True


    if scan_events >= 5:

        evidence.append(

            f"Multiple port scanning attempts detected ({scan_events})"

        )


    if blocked:

        evidence.append(

            "Firewall blocked suspicious source"

        )


    return evidence



def detect_phishing(logs):

    evidence = []

    suspicious_attachment = False
    macro_attempt = False
    payload_blocked = False


    for log in logs:

        message = log.message.lower()


        if "suspicious attachment" in message:

            suspicious_attachment = True


        if "macro execution" in message:

            macro_attempt = True


        if "malicious payload blocked" in message:

            payload_blocked = True



    if suspicious_attachment:

        evidence.append(

            "Suspicious email attachment detected"

        )


    if macro_attempt:

        evidence.append(

            "Office macro execution attempt detected"

        )


    if payload_blocked:

        evidence.append(

            "Endpoint security blocked malicious payload"

        )


    return evidence



def detect_insider_threat(logs):

    evidence = []

    unusual_access = False
    data_transfer = False
    account_suspended = False


    for log in logs:

        message = log.message.lower()


        if "unusual file access" in message:

            unusual_access = True


        if "large data transfer" in message:

            data_transfer = True


        if "account temporarily suspended" in message:

            account_suspended = True



    if unusual_access:

        evidence.append(

            "Unusual file access behavior detected"

        )


    if data_transfer:

        evidence.append(

            "Potential data exfiltration activity detected"

        )


    if account_suspended:

        evidence.append(

            "User account was suspended by security"

        )


    return evidence