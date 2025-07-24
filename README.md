---
  ![Process Diagram](https://github.com/Gr3ytrac3/Guard-Mount---External-Peripheral-Scanner/blob/b5dbbb53f08e5192246df2ff8e7643b0ae4676ab/guard-mount.png)


<h1 align="center">
  🛡️ Guard Mount
</h1>
<h4 align="center">
  Real-Time USB Threat Detection, Isolation & Authorization for Linux
</h4>

<p align="center">
  <code>RedKernel</code> • <code>Linux Security</code> • <code>Malware Prevention</code> • <code>Red Team Defense</code>
</p>

---

## 🔍 What is Guard Mount?

**Guard Mount** is a Linux-based real-time USB device monitor and malware scanner that detects, analyzes, and controls access to external peripherals (USBs, HDDs). It automatically scans newly inserted storage devices **before they mount**, checks for malicious or suspicious content (e.g. Rubber Ducky payloads, autorun scripts, hidden executables), and **requires sudo permission** before granting access.

---

## Features

✅ **Live USB Device Detection**  
✅ **Auto-Mount Blocker**  
✅ **Malware Scanning using ClamAV**  
✅ **Detection of Suspicious Scripts, Macros & Hidden Files**  
✅ **Rubber Ducky/BadUSB Identification (HID + Storage Check)**  
✅ **Terminal-based Threat Report with User Choice**  
✅ **Sudo Prompt Before Device is Allowed to Mount**  
✅ **Can Quarantine, Clean, Eject or Reject Devices**  
✅ **Systemd Integration for Background Monitoring**

---

## Example Terminal Output

```

─────────────────────────────────────────────
🛡️  Guard Mount - Threat Report
─────────────────────────────────────────────
📅 Date: Wed, 23 Jul 2025 — 18:22:41
📂 Device: /dev/sdb1 (Kingston USB Drive)
🔍 Scan Status: COMPLETED
🧠 Device Classification: Suspicious Storage Device

─────────────────────────────────────────────
🔬 SCAN RESULTS:

✅ Clean Files: 83
⚠️ Suspicious Files: 2
☠️ Malicious Files: 3

☠️ MALICIOUS FILES DETECTED:

\[1] /mnt/usb/hidden/.backdoor.sh            (Trojan.Shell.Backdoor)
\[2] /mnt/usb/docs/tax\_return\_2025.pdf.exe   (Worm.AutoExec.Dropper)
\[3] /mnt/usb/system/autorun.inf             (Malicious AutoRun Script)

⚠️ SUSPICIOUS FILES:

\[1] /mnt/usb/macro/invoice.docm             (Macro-Enabled Document)
\[2] /mnt/usb/bin/hidden\_payload             (High Entropy Binary)

─────────────────────────────────────────────
🛑 Auto-Mount Blocked.

🔐 Please authenticate to proceed.

Choose an action:
\[1] Allow Access (read-only)
\[2] Clean and Mount
\[3] Quarantine Entire Drive
\[4] Eject Device

````

---

## 📦 Installation

### 🔧 Requirements

- Python 3.8+
- Linux (Ubuntu, Kali, Arch, etc.)
- [ClamAV](https://www.clamav.net/) antivirus engine
- Required Python packages:
  - `pyudev`, `psutil`, `clamd`, `rich`, `colorama`

### 🧪 Setup Instructions

```bash
# Install ClamAV
sudo apt install clamav clamav-daemon -y
sudo freshclam  # Update virus definitions

# Clone the repo
git clone https://Gr3ytrac3/Guard-Mount---External-Peripheral-Scanner.git
cd guard-mount

# Install Python dependencies
pip install -r requirements.txt
````

---

## ▶️ Running USB Guardian

```bash
sudo python3 guard-mount/main.py
```

USB Guardian will now watch for inserted USB drives and immediately begin analysis.

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
Guard Mount - External Peripheral Scanner/
├── guard-mount/               ← Core Python modules
│   ├── detector.py             ← USB event monitor
│   ├── scanner.py              ← File/malware scanner
│   ├── reporter.py             ← Threat report & CLI UI
│   ├── isolator.py             ← Mount control
│   ├── authorizer.py           ← Sudo handling
│   └── main.py                 ← Entry point
│
├── config/                     ← Rule sets & settings
├── logs/                       ← Scan & runtime logs
├── system/guard-mount.service← systemd integration
├── assets/logo.txt             ← ASCII art (for fun)
├── requirements.txt            ← Python packages
└── README.md                   ← You’re here
```

---

## 🤝 Contributing

Contributions welcome! Whether you're submitting a pull request, improving detection heuristics, or creating a GUI wrapper — you’re helping improve Linux USB security.

---

## Ideas for Future Features

* GUI interface
* Integration with VirusTotal or hybrid-analysis
* Threat classification DB
* USB sandboxing (via firejail or QEMU)
* Audit log uploader (SIEM support)

---

## Author

**RedKernel**
💻 Offensive Security Artisan & Kernel Security Engineer

---

> “The most dangerous payloads are the ones you never see — until they run.”
> — *Guard Mount*
