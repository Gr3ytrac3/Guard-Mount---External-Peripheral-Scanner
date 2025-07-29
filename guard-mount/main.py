#!/usr/bin/env python3
"""
GuardMount - Main Entry Point
Kernel-Level External Device Interception & Threat Gatekeeper
"""

import sys
import os
from pathlib import Path
from utils import display_startup_sequence
from detector import monitor_usb_events  # Import your original function


def check_root_privileges():
    """Ensure script is running with proper privileges"""
    if os.geteuid() != 0:
        print("❌ GuardMount requires root privileges for kernel-level operations")
        print("   Please run with: sudo python3 main.py")
        sys.exit(1)


def check_dependencies():
    """Check if all required modules are available"""
    required_modules = ['pyudev', 'pathlib']
    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print(f"❌ Missing required modules: {', '.join(missing_modules)}")
        print("   Install with: pip install -r requirements.txt")
        sys.exit(1)


def main():
    """Main GuardMount entry point"""
    try:
        # Display startup sequence with logo
        display_startup_sequence()

        # Check system requirements
        print("🔍 Performing system checks...")
        check_root_privileges()
        check_dependencies()
        print("✅ System checks passed")

        # Start your original detector function
        print("🚀 Starting GuardMount detector...")
        monitor_usb_events()  # Call your original function

    except KeyboardInterrupt:
        print("\n🛡️  GuardMount shutdown initiated by user")
        print("✅ All monitoring processes stopped safely")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Critical error in GuardMount: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()