# SentLens

**SentLens** is a Python desktop cyber-incident investigation and Security Operations Center (SOC) training simulator. It generates synthetic security logs across common attack vectors, analyzes telemetry using rule-based detection logic, maps findings to the **MITRE ATT&CK** framework, enriches Indicators of Compromise (IOCs) via external threat intelligence, and recommends simulated containment playbooks.

> **Disclaimer:** SentLens is a standalone training and demonstration tool. All security events are synthetically generated in memory, and containment playbooks are simulation-only—the application does not ingest host logs, modify system configurations, or block live network traffic.

---

## Key Features

* **Synthetic Case Generation:** Generates realistic security incident scenarios mixed with baseline benign background events across four attack vectors:
  * **Brute-Force Attacks**
  * **Port Scanning**
  * **Phishing**
  * **Insider Threats**
* **Chronological Case Timeline:** Reconstructs and displays generated security and baseline events in chronological order for triage.
* **Rule-Based Detection & IOC Extraction:** Parses log entries using regular expressions (`re`) to detect suspicious patterns, extract Indicators of Compromise (IP addresses, usernames), calculate detection confidence scores, and map behaviors to **MITRE ATT&CK** techniques.
* **Asynchronous Threat Intelligence Enrichment:** Queries the **AbuseIPDB API** in a background thread (`threading`, `requests`) to retrieve IP reputation data without blocking the graphical interface.
* **Interactive Analytics & Reporting:** Displays embedded **Matplotlib** visualizations and structured incident reports with recommended remediation steps.
* **Simulated Containment Playbooks:** Demonstrates step-by-step response and containment workflows safely inside a sandboxed UI.

---

## Project Architecture

```text
SentLens/
├── src/
│   ├── main.py                  # Application entry point & dark theme configuration
│   ├── models/                  # Dataclass definitions for incidents and log entries
│   ├── engine/                  # Synthetic log & timestamp generation engine
│   │   └── attacks/             # Scenario generators (brute force, port scan, phishing, insider threat)
│   ├── analyzer/                # Regex IOC extraction, confidence scoring & MITRE ATT&CK mapping
│   ├── intelligence/            # Asynchronous AbuseIPDB API reputation lookup
│   ├── response/                # Simulated incident containment playbooks
│   ├── reports/                 # Incident report formatting & remediation guidance
│   └── ui/                      # CustomTkinter desktop interface, timeline & Matplotlib analytics
├── requirements.txt             # Pinned Python dependencies
└── README.md




Tech Stack
Language: Python 3

GUI Framework: CustomTkinter (tkinter)

Data Visualization: Matplotlib

Threat Intelligence Integration: REST API (requests), AbuseIPDB

Standard Library: re, dataclasses, datetime, threading, random, os

Installation & Setup
1. Clone the repository
Bash
git clone [https://github.com/](https://github.com/)<your-username>/SentLens.git
cd SentLens
2. Create and activate a virtual environment
Windows (PowerShell):

PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
macOS / Linux:

Bash
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
Bash
pip install -r requirements.txt
4. (Optional) Configure AbuseIPDB Threat Intelligence
To enable live IP reputation lookups, set your free AbuseIPDB API key as an environment variable before launching the app:

Windows (PowerShell):

PowerShell
$env:ABUSEIPDB_API_KEY="your_api_key_here"
macOS / Linux:

Bash
export ABUSEIPDB_API_KEY="your_api_key_here"
Usage
Launch the desktop application from the repository root:

Bash
python src/main.py
Typical Investigation Workflow
Click Generate New Case to simulate a mixed log dataset.

Inspect the Case Timeline to review raw events chronologically.

Run Analyze Current Case to extract IOCs, compute a confidence score, and view the MITRE ATT&CK classification.

Open Investigation and Analytics to inspect evidence, charts, and recommended actions.

(Optional) Click Enrich IP Reputation to query AbuseIPDB for extracted external IPs.

Run Execute Simulated Playbook to review example containment actions.


---

### How to Push This `README.md` to `main`
1. Open **`README.md`** in VS Code, paste the text above (updating `<your-username>`), and press **`Ctrl + S`**.
2. In your VS Code terminal (`Ctrl + ~`), run:
   ```powershell
   git add README.md
   git commit -m "Add comprehensive project documentation to README"
   git push origin main
