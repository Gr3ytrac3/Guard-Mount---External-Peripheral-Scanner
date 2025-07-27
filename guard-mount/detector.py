import pyudev
import time
import subprocess

def get_device_info(device):
    device_node = device.get('DEVNAME', 'Unknown')
    id_model = device.get('ID_MODEL', 'Unknown')
    id_vendor = device.get('ID_VENDOR', 'Unknown')
    serial = device.get('ID_SERIAL_SHORT', 'Unknown')

    return {
        'device_node': device_node,
        'model': id_model,
        'vendor': id_vendor,
        'serial': serial
    }

def is_storage_device(device):
    return 'ID_USB_DRIVER' in device and device['ID_USB_DRIVER'] == 'usb-storage'

def monitor_usb_events(callback):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')  # Only listen for block devices (e.g., USBs, HDDs)

    print("[USB Guardian] Listening for USB devices...")

    for device in iter(monitor.poll, None):
        if device.action == 'add' and is_storage_device(device):
            info = get_device_info(device)
            print(f"\n[!] Detected New Device: {info['vendor']} {info['model']} ({info['device_node']})")
            callback(info)

# Example callback function to trigger scanner
def device_detected_callback(info):
    print(f"-> Triggering scan for device {info['device_node']}... (this will be the scanner step)")

if __name__ == "__main__":
    monitor_usb_events(device_detected_callback)
