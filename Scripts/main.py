import csv
import json
import argparse
from pathlib import Path
from datetime import datetime

def load_policy(policy_path):
    with open(policy_path, 'r') as f:
        return json.load(f)

def load_inventory(inventory_path):
    devices = []
    with open(inventory_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            devices.append(row)
    return devices

def evaluate_config(config_text, policy):
    findings = []
    score = 100
    
    # Check SSH version
    if policy.get("ssh_version") == 2:
        if "ip ssh version 2" not in config_text:
            findings.append("[HIGH] SSH version 2 not explicitly enabled")
            score -= 25
            
    # Check Telnet
    if not policy.get("telnet_allowed"):
        if "transport input telnet" in config_text or "line vty" in config_text and "telnet" in config_text:
            findings.append("[HIGH] Telnet management protocol enabled")
            score -= 25
            
    # Check HTTP Management
    if not policy.get("http_management_allowed"):
        if "ip http server" in config_text and "no ip http server" not in config_text:
            findings.append("[MEDIUM] Insecure HTTP management server enabled")
            score -= 25
            
    # Check Password Encryption
    if policy.get("password_encryption_required"):
        if "service password-encryption" not in config_text:
            findings.append("[LOW] Password encryption service not enabled")
            score -= 25
    # Check Banner
    if policy.get("banner_required"):
        if "banner motd" not in config_text:
            findings.append("[LOW] Regulatory login banner (MOTD) missing")
            score -= 10
    return max(score, 0), findings

def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    parser = argparse.ArgumentParser(description="Secure Network Automation & Compliance Engine")
    parser.add_argument("--inventory", default=str(BASE_DIR / "Data" / "devices.csv"), help="Path to device inventory CSV")
    parser.add_argument("--policy", default=str(BASE_DIR / "Policies" / "network_security_policy.json"), help="Path to security policy JSON")
    parser.add_argument("--config-dir", default=str(BASE_DIR / "Data" / "Configs"), help="Directory containing device configs")
    parser.add_argument("--report", default=str(BASE_DIR / "Reports" / "network_security_report.txt"), help="Path to output report")
    args = parser.parse_args()

    policy = load_policy(args.policy)
    devices = load_inventory(args.inventory)
    
    report_lines = [
        "=" * 50,
        "       SECURE NETWORK AUTOMATION REPORT",
        "=" * 50,
        f"\nAssessment Date: {datetime.now().strftime('%Y-%m-%d')}",
        f"Devices Assessed: {len(devices)}\n",
        "-" * 50,
        "DEVICE ASSESSMENT RESULTS",
        "-" * 50
    ]

    compliant_count = 0
    non_compliant_count = 0

    for dev in devices:
        hostname = dev["hostname"]
        config_file = Path(args.config_dir) / f"{hostname}.txt"
        
        if not config_file.exists():
            report_lines.append(f"\nDevice: {hostname} ({dev['ip_address']})")
            report_lines.append("Status: CONFIG NOT FOUND")
            continue
            
        config_text = config_file.read_text()
        score, findings = evaluate_config(config_text, policy)
        
        status = "COMPLIANT" if score == 100 else "NON-COMPLIANT"
        if score == 100:
            compliant_count += 1
        else:
            non_compliant_count += 1
            
        report_lines.append(f"\nDevice: {hostname} ({dev['ip_address']})")
        report_lines.append(f"Status: {status}")
        report_lines.append(f"Security Score: {score}%")
        
        if findings:
            report_lines.append("Findings:")
            for finding in findings:
                report_lines.append(f"  - {finding}")
        else:
            report_lines.append("Findings: None")

    report_lines.extend([
        "\n" + "-" * 50,
        "SUMMARY STATISTICS",
        "-" * 50,
        f"Compliant Devices     : {compliant_count}",
        f"Non-Compliant Devices : {non_compliant_count}",
        "=" * 50
    ])

    report_content = "\n".join(report_lines)
    
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_content)
    
    print(f"[+] Security report successfully generated at: {report_path}")

if __name__ == "__main__":
    main()