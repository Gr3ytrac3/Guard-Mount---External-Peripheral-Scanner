# detector.py

import pyudev
import time
import os
from scanner import scan_device
from reporter import display_report
from isolator import isolate_device, authorize_device


def get_device_info(device):
    props = device.properties
    device_node = props.get('DEVNAME', 'Unknown')
    id_model = props.get('ID_MODEL', 'Unknown')
    id_vendor = props.get('ID_VENDOR', 'Unknown')
    serial = props.get('ID_SERIAL_SHORT', 'Unknown')
    bus = props.get('ID_BUS', 'Unknown')

    return {
        'device_node': device_node,
        'model': id_model,
        'vendor': id_vendor,
        'serial': serial,
        'bus': bus
    }


def is_usb_storage_device(device):
    props = device.properties

    is_usb = props.get('ID_BUS') == 'usb'
    device_path = device.device_path or ''
    has_usb_in_path = '/usb' in device_path
    is_block_device = device.subsystem == 'block'
    device_type = props.get('DEVTYPE', '')
    is_partition = device_type == 'partition'  # <-- Add this

    if is_usb or has_usb_in_path:
        print(f"[DEBUG] Device: {device.device_node}")
        print(f"[DEBUG] USB Bus: {is_usb}")
        print(f"[DEBUG] USB in path: {has_usb_in_path}")
        print(f"[DEBUG] Block device: {is_block_device}")
        print(f"[DEBUG] Device type: {device_type}")
        print(f"[DEBUG] Subsystem: {device.subsystem}")

    # Only trigger handling for partitions now!
    return (is_usb or has_usb_in_path) and is_block_device and is_partition



def handle_new_device(device):
    info = get_device_info(device)
    device_node = info['device_node']

    print(f"\n[!] Detected New USB Storage Device:")
    print(f"    Vendor: {info['vendor']}")
    print(f"    Model: {info['model']}")
    print(f"    Device: {info['device_node']}")
    print(f"    Serial: {info['serial']}")
    print(f"    Bus: {info['bus']}")

    # Step 1: Force Unmount Immediately
    isolate_device(device_node)

    # Step 2: Proceed with Offline Scan
    print(f"[+] Proceeding with scan for {device_node} (offline)...")
    report = scan_device(device_node)
    user_action = display_report(report)

    # Step 3: If allowed, Remount Device
    if user_action == "1":
        authorize_device(device_node)
    elif user_action == "2":
        print("[+] Cleaning malicious files (placeholder action)...")
        authorize_device(device_node)
    elif user_action == "3":
        print("[+] Device remains quarantined and unmounted.")
    else:
        print("[+] No valid action selected, device remains isolated.")


def monitor_usb_events():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    print("[USB Guardian] Listening for USB devices...")
    print("[DEBUG] Monitoring block device events...")

    for device in iter(monitor.poll, None):
        print(f"[DEBUG] Event: {device.action} for {device.device_node}")

        if device.action == 'add':
            if is_usb_storage_device(device):
                handle_new_device(device)
            else:
                print(f"[DEBUG] Device {device.device_node} is not a USB storage device")


if __name__ == "__main__":
    try:
        monitor_usb_events()
    except KeyboardInterrupt:
        print("\n[USB Guardian] Monitoring stopped.")
    except Exception as e:
        print(f"[ERROR] {e}")
