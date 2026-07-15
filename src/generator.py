def generate_scenario(scenario_name):
    """
    Generates a simulated cyber incident scenario.
    Returns a dictionary containing scenario details.
    """

    if scenario_name == "brute_force":
        return {
            "name": "Brute Force Attack",
            "severity": "High",
            "logs": [
                "09:14:01 LOGIN FAILED - user: admin - IP: 192.168.1.25",
                "09:14:03 LOGIN FAILED - user: admin - IP: 192.168.1.25",
                "09:14:05 LOGIN FAILED - user: admin - IP: 192.168.1.25",
                "09:14:07 LOGIN FAILED - user: admin - IP: 192.168.1.25",
                "09:14:09 LOGIN FAILED - user: admin - IP: 192.168.1.25",
                "09:14:15 LOGIN SUCCESS - user: admin - IP: 192.168.1.25",
                "09:14:20 NEW ADMIN ACCOUNT CREATED - backup_admin"
            ]
        }

    return None