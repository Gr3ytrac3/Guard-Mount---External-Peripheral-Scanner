#!/usr/bin/env python3
"""
GuardMount - Enhanced USB Device Detector
Maintains original logic with improved display and logging
"""

import pyudev
import time
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from scanner import scan_device
from reporter import display_report
from isolator import isolate_device, authorize_device


class GuardMountDetector:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'detector.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_device_info(self, device):
        """Extract device information - maintains original logic"""
        props = device.properties
        device_node = props.get('DEVNAME', 'Unknown')
        id_model = props.get('ID_MODEL', 'Unknown').replace('_', ' ')
        id_vendor = props.get('ID_VENDOR', 'Unknown').replace('_', ' ')
        serial = props.get('ID_SERIAL_SHORT', 'Unknown')
        bus = props.get('ID_BUS', 'Unknown')

        # Additional useful info for enhanced display
        filesystem = props.get('ID_FS_TYPE', 'Unknown')
        label = props.get('ID_FS_LABEL', 'Unknown')
        uuid = props.get('ID_FS_UUID', 'Unknown')
        vendor_id = props.get('ID_VENDOR_ID', 'Unknown')
        product_id = props.get('ID_MODEL_ID', 'Unknown')

        return {
            'device_node': device_node,
            'model': id_model,
            'vendor': id_vendor,
            'serial': serial,
            'bus': bus,
            'filesystem': filesystem,
            'label': label,
            'uuid': uuid,
            'vendor_id': vendor_id,
            'product_id': product_id,
            'timestamp': datetime.now().isoformat()
        }

    def is_usb_storage_device(self, device):
        """USB storage detection - maintains your original logic exactly"""
        props = device.properties

        is_usb = props.get('ID_BUS') == 'usb'
        device_path = device.device_path or ''
        has_usb_in_path = '/usb' in device_path
        is_block_device = device.subsystem == 'block'
        device_type = props.get('DEVTYPE', '')
        is_partition = device_type == 'partition'  # Your key logic - target partitions

        if is_usb or has_usb_in_path:
            self.logger.debug(f"Device: {device.device_node}")
            self.logger.debug(f"USB Bus: {is_usb}")
            self.logger.debug(f"USB in path: {has_usb_in_path}")
            self.logger.debug(f"Block device: {is_block_device}")
            self.logger.debug(f"Device type: {device_type}")
            self.logger.debug(f"Subsystem: {device.subsystem}")

        # Only trigger handling for partitions - your original logic
        return (is_usb or has_usb_in_path) and is_block_device and is_partition

    def print_detection_banner(self, info):
        """Enhanced visual display while maintaining workflow"""
        print("\n" + "═" * 75)
        print("🛡️  GuardMount - External Device Intercepted")
        print("═" * 75)
        print(f"📅 Date: {datetime.now().strftime('%a, %d %b %Y — %H:%M:%S')}")
        print(f"📂 Device: {info['device_node']}")
        print(f"🏷️  Model: {info['vendor']} {info['model']}")
        print(f"🔢 Serial: {info['serial']}")
        print(f"🆔 VID:PID: {info['vendor_id']}:{info['product_id']}")
        print(f"💾 Filesystem: {info['filesystem']}")
        if info['label'] != 'Unknown':
            print(f"🏷️  Label: {info['label']}")
        print(f"🔗 Bus: {info['bus']}")
        print("═" * 75)
        print("🚨 AUTO-MOUNT BLOCKED - Initiating Security Protocol")
        print("═" * 75)

    def log_device_event(self, info, stage):
        """Log device events for audit trail"""
        log_entry = {
            'event': 'usb_device_event',
            'stage': stage,
            'timestamp': info['timestamp'],
            'device_info': info
        }

        # Write to JSON log
        with open(self.log_dir / 'device_events.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def handle_new_device(self, device):
        """Enhanced device handling - maintains your original workflow exactly"""
        info = self.get_device_info(device)
        device_node = info['device_node']

        # Enhanced visual display
        self.print_detection_banner(info)

        # Log detection event
        self.log_device_event(info, 'detected')

        # Step 1: Force Unmount Immediately (your original logic)
        print("🔒 Step 1: Isolating device from system...")
        isolate_device(device_node)
        self.log_device_event(info, 'isolated')

        # Step 2: Proceed with Offline Scan (your original logic)
        print(f"🔍 Step 2: Initiating offline threat scan for {device_node}...")
        print("─" * 75)

        report = scan_device(device_node)
        self.log_device_event(info, 'scanned')

        user_action = display_report(report)
        self.log_device_event(info, f'user_decision_{user_action}')

        # Step 3: If allowed, Remount Device (your original logic)
        print("\n" + "─" * 75)
        print("🔐 Step 3: Processing user decision...")

        if user_action == "1":
            print("✅ User authorized read-only access")
            authorize_device(device_node)
            self.log_device_event(info, 'authorized_readonly')
        elif user_action == "2":
            print("🧹 User requested cleaning malicious files...")
            # Your placeholder action maintained
            authorize_device(device_node)
            self.log_device_event(info, 'authorized_cleaned')
        elif user_action == "3":
            print("🚫 Device quarantined - remains unmounted")
            self.log_device_event(info, 'quarantined')
        else:
            print("❌ No valid action selected - device remains isolated")
            self.log_device_event(info, 'rejected')

        print("═" * 75)
        print("🛡️  GuardMount Protocol Complete")
        print("═" * 75)

    def monitor_usb_events(self):
        """Main monitoring loop - maintains your original logic"""
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('block')  # Your original filter

        print("🛡️  GuardMount - Kernel-Level USB Guardian")
        print("Intercepting external storage devices before mount...")
        print("Press Ctrl+C to stop monitoring\n")
        self.logger.info("GuardMount detector initialized - monitoring block devices")

        try:
            for device in iter(monitor.poll, None):
                self.logger.debug(f"Event: {device.action} for {device.device_node}")

                if device.action == 'add':
                    if self.is_usb_storage_device(device):
                        self.handle_new_device(device)
                    else:
                        self.logger.debug(f"Device {device.device_node} is not a USB storage partition")

        except KeyboardInterrupt:
            print("\n🛡️  GuardMount monitoring stopped by user")
            self.logger.info("GuardMount detector stopped by user")
        except Exception as e:
            print(f"❌ [ERROR] {e}")
            self.logger.error(f"Detector error: {e}")


# Maintain your original standalone execution
if __name__ == "__main__":
    detector = GuardMountDetector()
    detector.monitor_usb_events()