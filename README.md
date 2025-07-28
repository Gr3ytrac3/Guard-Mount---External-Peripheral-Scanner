---

![Process Diagram](https://github.com/Gr3ytrac3/Guard-Mount---External-Peripheral-Scanner/blob/b5dbbb53f08e5192246df2ff8e7643b0ae4676ab/guard-mount.png)

<h1 align="center">
  🛡️ GuardMount
</h1>
<h4 align="center">
  Kernel-Level External Device Interception & Threat Gatekeeper for Linux
</h4>

<p align="center">
  <code>RedKernel</code> • <code>Kernel Security</code> • <code>Pre-Mount Threat Interception</code> • <code>Advanced Red Team Defense</code>
</p>

---

## 🔍 What is GuardMount?

**GuardMount** is a next-generation Linux security tool that intercepts all external peripheral devices (USBs, HDDs, BadUSB devices) **at the kernel level before they can mount**, scans their content for malicious payloads, and **requires explicit user authorization to proceed**.

Unlike traditional USB scanners that react **after** the device mounts, **GuardMount acts as a gatekeeper, blocking auto-mount events through custom UDEV rules**. It ensures that no device touches your filesystem without passing an in-depth threat analysis — effectively eliminating split-second payload execution vectors.

---

## 🚫 Why Pre-Mount Interception Matters

Modern attack vectors (BadUSB, Rubber Ducky payloads, autorun scripts) can exploit devices **the moment they are mounted**. A fraction of a second is enough to:

* Trigger silent autorun scripts
* Inject malicious HID commands
* Execute stealthy firmware payloads

GuardMount stops this by:

* **Intercepting kernel mount events (via UDEV control)**
* Scanning the device **before** the system interacts with it
* Giving you the final say to allow, deny, or quarantine the device

---

## 🔐 Core Features

✅ **Kernel-Level Device Interception (UDEV Rule Integration)**

✅ **Blocks Auto-Mount Until Scan & Authorization**

✅ **Rubber Ducky & HID Attack Prevention**

✅ **Full Content Analysis using ClamAV + Heuristic Rules**

✅ **Persistent Device Fingerprinting (Serial, VID/PID Check)**

✅ **Terminal-Based Threat Report & User Prompt**

✅ **Mount Devices Only After Approval (Read-Only Mode by Default)**

✅ **Systemd Integration for Persistent Background Monitoring**

---

## 🖥️ Example Terminal Flow

```
───────────────────────────────────────────────────────────────────────
🛡️  GuardMount - Threat Gatekeeper
───────────────────────────────────────────────────────────────────────
📅 Date: Wed, 23 Jul 2025 — 18:22:41
📂 Device: /dev/sdb1 (Kingston USB Drive)
🔍 Scan Status: COMPLETED
🧠 Device Classification: Suspicious Storage Device

───────────────────────────────────────────────────────────────────────
🔬 SCAN RESULTS:

✅ Clean Files: 83
⚠️ Suspicious Files: 2
☠️ Malicious Files: 3

☠️ MALICIOUS FILES DETECTED:

 [1] /media/usb/hidden/.backdoor.sh            (Trojan.Shell.Backdoor)
 [2] /media/usb/docs/tax_return_2025.pdf.exe   (Worm.AutoExec.Dropper)
 [3] /media/usb/system/autorun.inf             (Malicious AutoRun Script)

⚠️ SUSPICIOUS FILES:

 [1] /media/usb/macro/invoice.docm             (Macro-Enabled Document)
 [2] /media/usb/bin/hidden_payload             (High Entropy Binary)

───────────────────────────────────────────────────────────────────────
🛑 Auto-Mount Intercepted.

🔐 Authenticate to Proceed.

Choose an action:
 [1] Allow Access (read-only)
 [2] Clean and Mount
 [3] Quarantine Entire Drive
 [4] Eject Device

```

---

## 📦 Installation & Setup

### Requirements

* Python 3.8+
* Linux (Ubuntu, Kali, Arch, etc.)
* [ClamAV](https://www.clamav.net/)
* Python Packages:

  * `pyudev`, `psutil`, `clamd`, `rich`, `colorama`

### Installation Steps

```bash
# Install ClamAV
sudo apt install clamav clamav-daemon -y
sudo freshclam  # Update virus definitions

# Clone GuardMount Repository
git clone https://github.com/Gr3ytrac3/Guard-Mount---External-Peripheral-Scanner.git
cd guard-mount

# Install Python dependencies
pip install -r requirements.txt
```

### ⚡ UDEV Lockdown Setup

```bash
# Copy GuardMount's UDEV rule to block automount for USB storage
sudo cp system/99-guardmount.rules /etc/udev/rules.d/

# Reload UDEV rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

## ▶️ Running GuardMount

```bash
sudo python3 guard-mount/main.py
```

GuardMount will now control all external storage devices — detecting, scanning, and authorizing them **before they reach your system**.

---

## ⚙️ Optional: Install as a Systemd Daemon

```bash
# Copy service file
sudo cp system/guard-mount.service /etc/systemd/system/

# Enable and start the service
sudo systemctl daemon-reexec
sudo systemctl enable guard-mount
sudo systemctl start guard-mount
```

Check status:

```bash
sudo systemctl status guard-mount
```

---

## 📁 Project Structure

```plaintext
GuardMount - External Peripheral Scanner/
├── guard-mount/               ← Core Python Modules
│   ├── detector.py             ← USB Event Monitor
│   ├── scanner.py              ← File/Malware Scanner
│   ├── reporter.py             ← CLI Threat Report UI
│   ├── isolator.py             ← Mount Controller (Pre-Mount)
│   ├── authorizer.py           ← Sudo Handling & Permissions
│   └── main.py                 ← Entry Point
│
├── config/                     ← Heuristics & Detection Rules
├── system/
│   ├── 99-guardmount.rules     ← UDEV Auto-Mount Blocker
│   └── guard-mount.service     ← systemd Service File
├── logs/                       ← Scan & Runtime Logs
├── assets/logo.txt             ← ASCII Art Logo
├── requirements.txt            ← Python Packages
└── README.md                   ← You’re here
```

---

## 🚀 Future Enhancements

* Kernel Threat Simulator Mode
* USB Firmware Analyzer
* Live SIEM Upload Support
* Kernel-Level Device Sandbox
* Zero-Day Payload Detection Heuristics

---

## 🤝 Contributing

Pull Requests, Feedback, and Feature Suggestions are welcome. Join in refining a tool that can redefine how Linux handles USB security.

---

## Author

**RedKernel**
💻 Offensive Security Artisan & Kernel Security Engineer

> “Devices don’t earn trust by being plugged in. They earn trust by surviving scrutiny.”
> — *GuardMount Sentinel Philosophy*

---

## 🧱 Disclaimer

GuardMount is designed for educational and professional security purposes. Unauthorized usage on systems you don’t own or have permission to protect is prohibited.

---
