MITRE_MAPPING = {

    "Brute Force Attack": {

        "id": "T1110",

        "name": "Brute Force",

        "description": (
            "Adversaries attempt to gain access "
            "by repeatedly trying authentication attempts."
        )

    },


    "Port Scan": {

        "id": "T1046",

        "name": "Network Service Discovery",

        "description": (
            "Adversaries scan networks to identify "
            "available services and systems."
        )

    },


    "Phishing Attack": {

        "id": "T1566",

        "name": "Phishing",

        "description": (
            "Adversaries use phishing messages "
            "to gain initial access."
        )

    },


    "Insider Threat": {

        "id": "T1078",

        "name": "Valid Accounts",

        "description": (
            "Adversaries abuse legitimate accounts "
            "to access systems."
        )

    }

}


def get_mitre_info(attack_type):

    return MITRE_MAPPING.get(

        attack_type,

        {

            "id": "Unknown",

            "name": "Unknown",

            "description": (
                "No MITRE ATT&CK mapping available."
            )

        }

    )