import os
import subprocess
import pyudev
import hashlib

MOUNT_DIR = "/mnt/usb_guardian"
SUSPICIOUS_EXTENSIONS = [".exe", ".bat", ".cmd", ".vbs", ".sh", ".ps1", ".scr", ".jar", ".docm"]
AUTORUN_FILE = "autorun.inf"
ENTROPY_THRESHOLD = 7.5  # High entropy indicates possible binary payloads

def get_first_partition(device_node):
    context = pyudev.Context()
    device = pyudev.Device.from_device_file(context, device_node)
    for child in device.children:
        if child.device_type == 'partition':
            return child.device_node
    return None

def get_mount_point(device_node):
    result = subprocess.run(['lsblk', '-no', 'MOUNTPOINT', device_node], capture_output=True, text=True)
    mountpoint = result.stdout.strip()
    return mountpoint if mountpoint else None

def mount_device(device_node):
    existing_mount = get_mount_point(device_node)
    if existing_mount:
        print(f"[+] Device is already mounted at {existing_mount}")
        return existing_mount  # Return existing mount path

    partition = get_first_partition(device_node)
    if not partition:
        print("[ERROR] No partitions found on device.")
        return None

    if not os.path.exists(MOUNT_DIR):
        os.makedirs(MOUNT_DIR)

    print(f"[+] Mounting {partition} to {MOUNT_DIR} as read-only...")
    try:
        subprocess.run(["mount", "-o", "ro", partition, MOUNT_DIR], check=True)
        print("[+] Mounted successfully.")
        return MOUNT_DIR
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to mount partition.")
        return None


def unmount_device():
    print(f"[+] Unmounting {MOUNT_DIR}...")
    subprocess.run(["umount", MOUNT_DIR], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def clamav_scan(mount_path):
    print("[+] Starting ClamAV scan...")
    result = subprocess.run(["clamscan", "-r", "--no-summary", mount_path], capture_output=True, text=True)
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

def heuristic_scan(mount_path):
    suspicious_files = []
    autorun_detected = False
    total_files = 0

    for root, dirs, files in os.walk(mount_path):
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)

            if file.lower() == AUTORUN_FILE:
                autorun_detected = True
                suspicious_files.append({'path': file_path, 'reason': 'Autorun Script'})

            if any(file.lower().endswith(ext) for ext in SUSPICIOUS_EXTENSIONS):
                suspicious_files.append({'path': file_path, 'reason': 'Suspicious File Extension'})

            if file.startswith('.'):
                suspicious_files.append({'path': file_path, 'reason': 'Hidden File'})

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

    mount_path = mount_device(device_node)
    if not mount_path:
        return scan_summary

    try:
        scan_summary["malicious"] = clamav_scan(mount_path)
        suspicious_files, total_files, autorun_detected = heuristic_scan(mount_path)
        scan_summary["suspicious"] = suspicious_files
        scan_summary["clean_count"] = total_files - len(scan_summary["malicious"]) - len(scan_summary["suspicious"])

    finally:
        if mount_path == MOUNT_DIR:  # Only unmount if WE mounted it.
            unmount_device()

    return scan_summary

