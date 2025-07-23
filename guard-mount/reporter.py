# scan_report.py

import datetime
import textwrap

# Simulated scan data (replace with real data later)
scan_result = {
    "device": "/dev/sdb1",
    "label": "Kingston USB Drive",
    "malicious": [
        { "path": "/mnt/usb/hidden/.backdoor.sh", "threat": "Trojan.Shell.Backdoor" },
        { "path": "/mnt/usb/docs/tax_return_2025.pdf.exe", "threat": "Worm.AutoExec.Dropper" },
        { "path": "/mnt/usb/system/autorun.inf", "threat": "Malicious AutoRun Script" }
    ],
    "suspicious": [
        { "path": "/mnt/usb/macro/invoice.docm", "reason": "Macro-Enabled Document" },
        { "path": "/mnt/usb/bin/hidden_payload", "reason": "High Entropy Binary" }
    ],
    "clean_count": 83
}

def print_header():
    print("─" * 50)
    print("      🛡️  Guard Mount - Threat Report")
    print("─" * 50)
    print(f"📅 Date: {datetime.datetime.now().strftime('%a, %d %b %Y — %H:%M:%S')}")
    print(f"📂 Device: {scan_result['device']} ({scan_result['label']})")
    print("🔍 Scan Status: COMPLETED")
    print("🧠 Device Classification: Suspicious Storage Device")
    print()

def print_results():
    print("─" * 50)
    print("🔬 SCAN RESULTS:")
    print()
    print(f"✅ Clean Files: {scan_result['clean_count']}")
    print(f"⚠️ Suspicious Files: {len(scan_result['suspicious'])}")
    print(f"☠️ Malicious Files: {len(scan_result['malicious'])}")
    print()

    print("─" * 50)
    print("☠️ MALICIOUS FILES DETECTED:")
    print()
    for i, item in enumerate(scan_result['malicious'], 1):
        print(f"  [{i}] {item['path']:<50} ({item['threat']})")
    print()

    print("⚠️ SUSPICIOUS FILES:")
    print()
    for i, item in enumerate(scan_result['suspicious'], 1):
        print(f"  [{i}] {item['path']:<50} ({item['reason']})")
    print()

def prompt_user():
    print("─" * 50)
    print("🛑 Auto-Mount Blocked.\n")
    print("🔐 Please authenticate to proceed.\n")
    print("Choose an action:")
    print("  [1] Allow Access (mount as read-only)")
    print("  [2] Clean and Mount (remove malicious files)")
    print("  [3] Quarantine Entire Drive")
    print("  [4] Eject Device")
    print("  [5] View Full Report")

    choice = input("\n👉 Your choice: ").strip()
    return choice

def main():
    print_header()
    print_results()
    user_choice = prompt_user()

    print("\nYou selected:", user_choice)
    if user_choice == "1":
        print("🔓 Mounting device as read-only...")
    elif user_choice == "2":
        print("🧹 Cleaning and mounting device...")
    elif user_choice == "3":
        print("📦 Quarantining device...")
    elif user_choice == "4":
        print("🔌 Ejecting device...")
    elif user_choice == "5":
        print("📄 Displaying full report... (not implemented)")
    else:
        print("❌ Invalid option.")

if __name__ == "__main__":
    main()
