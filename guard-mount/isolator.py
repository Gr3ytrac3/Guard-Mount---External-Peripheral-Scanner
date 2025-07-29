# isolator.py

import os
import subprocess


def authorize_usb_device(usb_device_path):
    """
    Re-authorizes a blocked USB device after passing security scan.
    """
    device_id = usb_device_path.split('/')[-1]
    authorized_path = f"/sys/bus/usb/devices/{device_id}/authorized"

    if os.path.exists(authorized_path):
        try:
            print(f"[+] Authorizing USB device {device_id}...")
            with open(authorized_path, 'w') as f:
                f.write('1')
            print("[+] Device authorized successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to authorize device: {e}")
    else:
        print(f"[ERROR] Device authorization path not found: {authorized_path}")


def mount_device(device_node, mount_point, read_only=True):
    os.makedirs(mount_point, exist_ok=True)

    mount_options = "ro" if read_only else "rw"

    print(f"[+] Mounting {device_node} to {mount_point} as {mount_options}...")
    cmd = ["mount", "-o", mount_options, device_node, mount_point]

    try:
        subprocess.run(cmd, check=True)
        print("[+] Device mounted successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to mount device: {e}")
        return False


def unmount_device(mount_point):
    print(f"[-] Unmounting {mount_point}...")
    try:
        subprocess.run(["umount", mount_point], check=True)
        print("[-] Device unmounted successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to unmount device: {e}")
        return False


def eject_device(device_node):
    print(f"[-] Ejecting {device_node}...")
    try:
        subprocess.run(["udisksctl", "power-off", "-b", device_node], check=True)
        print("[-] Device ejected successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to eject device: {e}")


def is_device_mounted(device_node):
    result = subprocess.run(["lsblk", "-no", "MOUNTPOINT", device_node], capture_output=True, text=True)
    return result.stdout.strip() != ""


def resolve_sysfs_usb_path(device_node):
    """
    Maps a /dev/sdX node to its corresponding /sys/bus/usb/devices/usbX path.
    """
    try:
        real_path = os.path.realpath(device_node)
        sys_block_path = real_path.replace('/dev/', '/sys/class/block/')

        # Walk up the device chain to find usb device
        current = sys_block_path
        for _ in range(5):  # Max depth to walk up
            parent = os.path.dirname(current)
            if 'usb' in parent:
                print(f"[DEBUG] Resolved USB sysfs path: {parent}")
                return parent
            current = parent
        print("[ERROR] USB sysfs path could not be resolved.")
        return None

    except Exception as e:
        print(f"[ERROR] Exception in resolving sysfs path: {e}")
        return None


if __name__ == "__main__":
    print("[!] Isolator module. Not meant to be run standalone.")
