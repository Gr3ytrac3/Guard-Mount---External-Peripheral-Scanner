import os
import subprocess
import hashlib

# CONFIG
MOUNT_DIR = "/mnt/usb_guardian"
SUSPICIOUS_EXTENSIONS = [".exe", ".bat", ".cmd", ".vbs", ".sh", ".ps1", ".scr", ".jar", ".docm"]
AUTORUN_FILE = "autorun.inf"
ENTROPY_THRESHOLD = 7.5  # High entropy indicates possible binary payloads

def mount_device(device_node):
    if not os.path.exists(MOUNT_DIR):
        os.makedirs(MOUNT_DIR)

    print(f"[+] Mounting {device_node} to {MOUNT_DIR} as read-only...")
    try:
        subprocess.run(["mount", "-o", "ro", device_node, MOUNT_DIR], check=True)
        print("[+] Mounted successfully.")
        return True
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to mount device.")
        return False

def unmount_device():
    print(f"[+] Unmounting {MOUNT_DIR}...")
    subprocess.run(["umount", MOUNT_DIR], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def clamav_scan():
    print("[+] Starting ClamAV scan...")
    result = subprocess.run(["clamscan", "-r", "--no-summary", MOUNT_DIR], capture_output=True, text=True)
    malicious_files = []
    for line in result.stdout.strip().split("\n"):
        if "FOUND" in line:
            file_path, threat = line.split(":")
            threat = threat.replace(" FOUND", "").strip()
            malicious_files.append({'path': file_path.strip(), 'threat': threat})
    return malicious_files

def calculate_entropy(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    if not data:
        return 0
    entropy = -sum((data.count(byte) / len(data)) * (data.count(byte) / len(data)).bit_length() for byte in set(data))
    return entropy

def heuristic_scan():
    suspicious_files = []
    autorun_detected = False
    total_files = 0

    for root, dirs, files in os.walk(MOUNT_DIR):
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)

            # Detect autorun.inf
            if file.lower() == AUTORUN_FILE:
                autorun_detected = True
                suspicious_files.append({'path': file_path, 'reason': 'Autorun Script'})

            # Suspicious extensions
            if any(file.lower().endswith(ext) for ext in SUSPICIOUS_EXTENSIONS):
                suspicious_files.append({'path': file_path, 'reason': 'Suspicious File Extension'})

            # Hidden files or payloads
            if file.startswith('.'):
                suspicious_files.append({'path': file_path, 'reason': 'Hidden File'})

            # High entropy binaries
            try:
                entropy = calculate_entropy(file_path)
                if entropy >= ENTROPY_THRESHOLD:
                    suspicious_files.append({'path': file_path, 'reason': f'High Entropy ({entropy:.2f})'})
            except Exception as e:
                print(f"[ERROR] Could not calculate entropy for {file_path}: {e}")

    return suspicious_files, total_files, autorun_detected

def scan_device(device_node):
    scan_summary = {
        "device": device_node,
        "malicious": [],
        "suspicious": [],
        "clean_count": 0
    }

    if not mount_device(device_node):
        return scan_summary

    try:
        # ClamAV Scan
        scan_summary["malicious"] = clamav_scan()

        # Heuristics
        suspicious_files, total_files, autorun_detected = heuristic_scan()
        scan_summary["suspicious"] = suspicious_files
        scan_summary["clean_count"] = total_files - len(scan_summary["malicious"]) - len(scan_summary["suspicious"])

    finally:
        unmount_device()

    return scan_summary

if __name__ == "__main__":
    # Example Test Run
    device_node = "/dev/sdb1"  # Replace this with actual device node for testing
    report = scan_device(device_node)
    print(report)
