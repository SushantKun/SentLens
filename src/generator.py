def generate_scenario(scenario_name):
    """
    Generates a simulated cyber incident scenario.
    """

    scenarios = {

        "brute_force": {
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
        },

        "port_scan": {
            "name": "Port Scan",
            "severity": "Medium",
            "logs": [
                "10:01:10 TCP SYN to port 21",
                "10:01:11 TCP SYN to port 22",
                "10:01:12 TCP SYN to port 23",
                "10:01:13 TCP SYN to port 80",
                "10:01:14 TCP SYN to port 443",
                "10:01:15 TCP SYN to port 3389"
            ]
        },

        "phishing": {
            "name": "Phishing Attack",
            "severity": "High",
            "logs": [
                "11:30 Email received from support@micros0ft-login.com",
                "11:32 User clicked suspicious link",
                "11:33 Credentials submitted",
                "11:35 Login from unknown IP"
            ]
        },

        "insider_threat": {
            "name": "Insider Threat",
            "severity": "Critical",
            "logs": [
                "15:00 Employee accessed HR database",
                "15:02 Exported confidential records",
                "15:05 USB device connected",
                "15:08 Large file copied to removable drive"
            ]
        }

    }

    return scenarios.get(scenario_name)