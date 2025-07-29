#!/usr/bin/env python3
"""
GuardMount Utilities
Shared functions for logo display and common operations
"""

import os
from pathlib import Path


def display_guardmount_logo():
    """Display the GuardMount ASCII logo"""
    try:
        # Try to find logo file in multiple locations
        possible_paths = [
            Path('assets/logo.txt'),
            Path('../assets/logo.txt'),
            Path('guard-mount/assets/logo.txt'),
            Path('./assets/logo.txt')
        ]

        logo_path = None
        for path in possible_paths:
            if path.exists():
                logo_path = path
                break

        if logo_path:
            with open(logo_path, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            # Fallback banner if logo file not found
            display_fallback_banner()

    except Exception as e:
        print(f"Warning: Could not display logo: {e}")
        display_fallback_banner()


def display_fallback_banner():
    """Display a simple fallback banner"""
    print("\n" + "═" * 80)
    print("🛡️  GuardMount - Kernel-Level External Device Interception")
    print("   & Threat Gatekeeper for Linux Systems")
    print("   Author: RedKernel")
    print("═" * 80)
    print('"Devices don\'t earn trust by being plugged in.')
    print(' They earn trust by surviving scrutiny."')
    print("═" * 80)


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_startup_sequence():
    """Display complete startup sequence with logo"""
    clear_screen()
    display_guardmount_logo()
    print("\n🔧 Initializing GuardMount security systems...")
    print("📡 Loading device monitoring components...")
    print("🛡️ Engaging kernel-level interception...")
    print("✅ GuardMount ready for deployment")
    print("\n" + "─" * 60)