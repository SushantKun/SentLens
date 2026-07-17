def calculate_confidence(evidence, attack_type):

    score = 0


    for item in evidence:

        text = item.lower()


        # Authentication attacks
        if "failed login" in text:
            score += 30

        if "successful login" in text:
            score += 20

        if "admin" in text:
            score += 20


        # Network attacks
        if "port scanning" in text:
            score += 40

        if "blocked" in text:
            score += 30


        # Phishing
        if "attachment" in text:
            score += 30

        if "macro" in text:
            score += 30

        if "payload" in text:
            score += 30


        # Insider threat
        if "file access" in text:
            score += 30

        if "data exfiltration" in text:
            score += 40

        if "suspended" in text:
            score += 20



    # Attack-specific minimum confidence boosts

    if attack_type == "Port Scan":

        if len(evidence) >= 2:
            score += 20


    elif attack_type == "Brute Force Attack":

        if len(evidence) >= 2:
            score += 15


    elif attack_type == "Phishing Attack":

        if len(evidence) >= 2:
            score += 15


    elif attack_type == "Insider Threat":

        if len(evidence) >= 2:
            score += 15



    if score > 100:

        score = 100


    return score