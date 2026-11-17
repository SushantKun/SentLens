def execute_playbook(result):
    """
    Simulated containment only.
    This function does not alter real accounts, hosts, networks, or APIs.
    """

    indicators = result.get("indicators", {})
    ips = indicators.get("ips", [])
    users = indicators.get("users", [])

    target_ip = ips[0] if ips else "unavailable IP"
    target_user = users[0] if users else "unavailable user"

    actions_by_attack = {
        "Brute Force Attack": [
            f"Simulated: blocking source IP {target_ip}.",
            f"Simulated: revoking active sessions for {target_user}.",
            "Simulated: requiring a password reset and MFA review.",
        ],
        "Port Scan": [
            f"Simulated: adding firewall deny rule for {target_ip}.",
            "Simulated: increasing IDS monitoring for related probes.",
            "Simulated: opening a network-exposure review ticket.",
        ],
        "Phishing Attack": [
            f"Simulated: revoking active sessions for {target_user}.",
            "Simulated: quarantining matching email messages.",
            "Simulated: blocking the suspicious sender domain or URL.",
        ],
        "Insider Threat": [
            f"Simulated: temporarily restricting access for {target_user}.",
            "Simulated: preserving file-access and transfer logs.",
            "Simulated: escalating to security and HR review.",
        ],
    }

    return {
        "mode": "SIMULATION ONLY",
        "status": "completed",
        "actions": actions_by_attack.get(
            result["attack"],
            ["Simulated: opening an incident-review ticket."],
        ),
    }