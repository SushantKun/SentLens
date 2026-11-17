from engine.attacks import (
    brute_force,
    port_scan,
    phishing,
    insider_threat,
)


ATTACKS = {

    "Brute Force Attack": {

        "severity": "High",

        "source": "Windows Server",

        "generator": brute_force.generate

    },

    "Port Scan": {

        "severity": "Medium",

        "source": "Firewall",

        "generator": port_scan.generate

    },

    "Phishing Attack": {

        "severity": "High",

        "source": "Email Gateway",

        "generator": phishing.generate

    },

    "Insider Threat": {

        "severity": "Critical",

        "source": "Active Directory",

        "generator": insider_threat.generate

    }

}