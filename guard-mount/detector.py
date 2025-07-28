import pyudev
import subprocess
from scanner import scan_device
from reporter import display_report

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
    is_disk = device_type == 'disk'

    if is_usb or has_usb_in_path:
        print(f"[DEBUG] Device: {device.device_node}")
        print(f"[DEBUG] USB Bus: {is_usb}")
        print(f"[DEBUG] USB in path: {has_usb_in_path}")
        print(f"[DEBUG] Block device: {is_block_device}")
        print(f"[DEBUG] Device type: {device_type}")
        print(f"[DEBUG] Subsystem: {device.subsystem}")

    return (is_usb or has_usb_in_path) and is_block_device and is_disk

def device_detected_callback(info):
    print(f"-> Triggering scan for device {info['device_node']}...")
    report = scan_device(info['device_node'])
    display_report(report)

def monitor_usb_events(callback):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    print("[USB Guardian] Listening for USB devices...")
    print("[DEBUG] Monitoring block device events...")

    for device in iter(monitor.poll, None):
        print(f"[DEBUG] Event: {device.action} for {device.device_node}")

        if device.action == 'add':
            if is_usb_storage_device(device):
                info = get_device_info(device)
                print(f"\n[!] Detected New USB Storage Device:")
                print(f"    Vendor: {info['vendor']}")
                print(f"    Model: {info['model']}")
                print(f"    Device: {info['device_node']}")
                print(f"    Serial: {info['serial']}")
                print(f"    Bus: {info['bus']}")
                callback(info)
            else:
                print(f"[DEBUG] Device {device.device_node} is not a USB storage device")

if __name__ == "__main__":
    try:
        monitor_usb_events(device_detected_callback)
    except KeyboardInterrupt:
        print("\n[USB Guardian] Monitoring stopped.")
    except Exception as e:
        print(f"[ERROR] {e}")
