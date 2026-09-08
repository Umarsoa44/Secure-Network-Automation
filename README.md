```markdown
# Secure Network Automation & Configuration Validation Platform

![Platform Execution](Assets/Terminal_output.png)

## Overview
The **Secure Network Automation & Configuration Validation Platform** is a robust, enterprise-grade Python framework engineered to automate network compliance audits, streamline configuration management, and enforce rigorous security baselines across multi-vendor network topologies. 

By leveraging a decoupled **Policy-as-Code** architecture, the platform separates compliance rule definitions from execution logic. This ensures network engineers and security auditors can scale their defensive postures, eliminate human configuration drift, and instantly identify vulnerabilities across routers, switches, and firewalls without altering core program scripts.

## Core Architecture & Workflow
1. **Inventory Ingestion:** The platform reads structured device mappings from CSV files (`devices.csv`), identifying node roles, platforms, and associated configuration file paths.
2. **Configuration Parsing:** Raw configuration text files (stored in `Data/Configs/`) are loaded dynamically, representing current operational states or historical baselines.
3. **Policy-as-Code Engine:** Rules and security controls are defined centrally in a structured JSON schema (`network_security_policy.json`), allowing seamless modification of compliance requirements.
4. **Compliance Audit & Scoring:** The core script evaluates each device configuration line-by-line against security checks, calculating automated risk scores and categorizing findings into high, medium, and low severities.
5. **Persistent Reporting:** Audit outcomes are simultaneously output to the real-time terminal dashboard and written out to a persistent timestamped file within the `Reports/` directory.

## Key Features & Capabilities
* **Dynamic Policy Engine:** Centralizes security compliance rules into an editable JSON format, eliminating hardcoded validation logic.
* **Granular Risk Scoring:** Automatically evaluates security violations to quantify node-level risk postures.
* **Heterogeneous Asset Management:** Handles multi-vendor device configurations seamlessly using scalable inventory tracking.
* **Audit Trail Generation:** Produces clean, structured text reports suitable for compliance tracking, stakeholder reviews, and historical record-keeping.
* **Built-in Quality Assurance:** Features an integrated `unittest` suite (`Tests/test_validator.py`) ensuring continuous logic integrity and reliable code execution.

## Project Directory Structure
```text
Secure-Network-Automation/
│
├── Assets/                 # Visual project assets and documentation screenshots
│   ├── .gitkeep
│   └── Terminal_output.png
│
├── Backups/                # Historical configuration archives and pre-audit snapshots
│   ├── .gitkeep
│   └── EDGE-RTR-02_backup.txt
│
├── Data/                   # Core input data, device mappings, and raw configurations
│   ├── Configs/
│   │   ├── CORE-SW-02.txt
│   │   ├── DMZ-FW-02.txt
│   │   └── EDGE-RTR-02.txt
│   └── devices.csv
│
├── Policies/               # Centralized security control definitions (Policy-as-Code)
│   └── network_security_policy.json
│
├── Reports/                # Automated audit output logs and compliance summaries
│   └── network_security_report.txt
│
├── Scripts/                # Core execution logic and automation pipelines
│   └── main.py
│
├── Tests/                  # Automated unit test suite verifying validation logic
│   └── test_validator.py
│
└── README.md

```

## Security Policy Controls

The default policy engine inspects configurations for compliance with standard industry security baselines:

* **[HIGH] Secure Management Access:** Verifies that secure remote administration utilizes SSH version 2 (`ip ssh version 2`).
* **[HIGH] Cleartext Protocol Mitigation:** Identifies and flags legacy, unencrypted management protocols such as Telnet.
* **[MEDIUM] Web Management Services:** Detects enabled HTTP server instances (`ip http server`) that risk exposing device interfaces.
* **[LOW] Credential Protection:** Enforces local password encryption standards (`service password-encryption`).
* **[LOW] Regulatory Banners:** Validates the presence of mandatory legal or organizational MOTD warning banners.

## Installation & Setup

1. **Clone the Repository:**
```bash
git clone [https://github.com/Umar-Farooq-Shaikh/Secure-Network-Automation.git](https://github.com/Umar-Farooq-Shaikh/Secure-Network-Automation.git)
cd Secure-Network-Automation

```


2. **Verify Environment Requirements:** Ensure Python 3.10 or higher is installed on your local machine or automation server. No external third-party pip packages are required, as the platform relies entirely on Python's robust standard library.

## Usage Guide

### Running Compliance Audits

Execute the main automation pipeline from the root directory via your terminal or PowerShell:

```bash
python Scripts/main.py

```

### Executing Unit Tests

To verify the integrity of the validation logic and run the automated test suite, execute:

```bash
python -m unittest discover -s Tests

```

## Output & Reporting Example

Upon successful execution, the platform prints a summary dashboard to standard output and generates an audit log at **`Reports/network_security_report.txt`**.

## Future Roadmap

* Integration with network automation libraries (Netmiko/Napalm) for live device polling.
* Expansion of the JSON policy schema to cover advanced routing protocol security (BGP/OSPF authentication).
* Web-based dashboard interface for visualizing global compliance metrics.

---

*Developed as a portfolio project demonstrating modern network automation, software engineering best practices, and infrastructure security compliance.*

```

```
