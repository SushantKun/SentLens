import ipaddress
import os

import requests


ABUSEIPDB_CHECK_URL = "https://api.abuseipdb.com/api/v2/check"


def is_public_ip(ip_address):
    try:
        address = ipaddress.ip_address(ip_address)

        return not (
            address.is_private
            or address.is_loopback
            or address.is_multicast
            or address.is_reserved
            or address.is_unspecified
        )

    except ValueError:
        return False


def lookup_ip_reputation(ip_address):
    """
    Checks one public IP address against AbuseIPDB.

    The API key is read from the ABUSEIPDB_API_KEY environment variable.
    No API keys should be written inside source code.
    """

    api_key = os.getenv("ABUSEIPDB_API_KEY")

    if not api_key:
        return {
            "available": False,
            "status": "not_configured",
            "message": "Threat-intelligence API key is not configured.",
        }

    if not is_public_ip(ip_address):
        return {
            "available": False,
            "status": "skipped",
            "message": "Private or invalid IP addresses are not checked.",
        }

    headers = {
        "Accept": "application/json",
        "Key": api_key,
    }

    parameters = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90,
        "verbose": "",
    }

    try:
        response = requests.get(
            ABUSEIPDB_CHECK_URL,
            headers=headers,
            params=parameters,
            timeout=8,
        )
        response.raise_for_status()

        data = response.json()["data"]

        return {
            "available": True,
            "status": "complete",
            "provider": "AbuseIPDB",
            "ip_address": data.get("ipAddress", ip_address),
            "abuse_confidence_score": data.get(
                "abuseConfidenceScore",
                0,
            ),
            "total_reports": data.get("totalReports", 0),
            "country_code": data.get("countryCode", "Unknown"),
            "isp": data.get("isp", "Unknown"),
            "domain": data.get("domain", "Unknown"),
            "last_reported_at": data.get(
                "lastReportedAt",
                "No reports returned",
            ),
        }

    except requests.RequestException as error:
        return {
            "available": False,
            "status": "error",
            "message": f"Threat-intelligence lookup failed: {error}",
        }