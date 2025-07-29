# isolator.py

import os
import subprocess

def force_unmount(device_node):
    try:
        print(f"[+] Attempting to unmount {device_node}...")
        subprocess.run(['udisksctl', 'unmount', '-b', device_node], check=True)
        print(f"[+] Device {device_node} unmounted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to unmount {device_node}: {e}")

def remount_device(device_node):
    try:
        print(f"[+] Attempting to remount {device_node}...")
        subprocess.run(['udisksctl', 'mount', '-b', device_node], check=True)
        print(f"[+] Device {device_node} remounted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to remount {device_node}: {e}")

def isolate_device(device_node):
    force_unmount(device_node)

def authorize_device(device_node):
    remount_device(device_node)
