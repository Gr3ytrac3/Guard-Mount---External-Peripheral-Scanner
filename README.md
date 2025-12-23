![Process Diagram](https://github.com/Gr3ytrac3/Guard-Mount---External-Peripheral-Scanner/blob/b5dbbb53f08e5192246df2ff8e7643b0ae4676ab/guard-mount.png)

<h1 align="center">
  🛡️ GuardMount (Active Rebuild)
</h1>
<h4 align="center">
  Kernel-Adjacent External Device Interception & Pre-Mount Security Gatekeeper for Linux
</h4>

<p align="center">
  <code>RedKernel</code> • <code>Linux Internals</code> • <code>udev</code> • <code>Pre-Mount Access Control</code> • <code>Offensive / Defensive Security</code>
</p>

---

## What is GuardMount?

**GuardMount** is a Linux security project designed to **intercept external peripheral devices at the earliest safe point in userspace**, *before* they are mounted or allowed to interact with the system.

It acts as a **pre-mount security gatekeeper**, enforcing a **default-deny policy** on removable devices (USB storage, external drives, BadUSB-class devices) and requiring **explicit authorization** before access is granted.

Rather than reacting to threats *after* a device is mounted, GuardMount focuses on **control over device access**, ensuring that no external peripheral can touch the filesystem without first passing through a security decision layer.

---

## Design Philosophy

GuardMount is built on one core security principle:

> **Control beats detection.**

Most USB security tools attempt to *scan* devices after they are already mounted. This is too late against modern attack vectors where malicious behavior can occur within milliseconds of insertion.

GuardMount instead enforces **early interception**, using Linux’s device event infrastructure to block automatic device interaction and shift the decision to a controlled, auditable process.

---

## Why Pre-Mount Interception Matters

Modern external device attacks do not wait for user interaction.

A newly inserted device can:
- Execute autorun-style payloads
- Emulate HID devices (Rubber Ducky / BadUSB)
- Exploit auto-mount behavior
- Trigger filesystem or parser vulnerabilities

Once a device is mounted, **the trust boundary is already crossed**.

GuardMount prevents this by:
- Intercepting device events **before mount**
- Blocking auto-mount at the udev level
- Holding the device in a restricted state until a verdict is reached

If no decision is made — the device remains blocked.

---

## Core Architecture (High-Level)

GuardMount is intentionally designed as a **layered system**, separating enforcement from policy:

- **Enforcement Core (C)**
  A minimal, deterministic daemon that listens for device events via `libudev`, blocks auto-mount, and enforces allow/deny decisions.

- **Policy & Intelligence Layer (Userspace)**
  Performs scanning, reporting, and user interaction. This layer can fail safely without compromising enforcement.

- **System Integration Layer**
  udev rules and systemd services ensure GuardMount runs persistently and intercepts devices consistently across reboots.

This separation ensures that **failure does not equal compromise**.

---

## What GuardMount Does

- Intercepts external block devices at insertion time
- Prevents automatic mounting and implicit trust
- Maintains a controlled decision point for each device
- Allows devices only after explicit authorization
- Enforces conservative mount options by default

---

## What GuardMount Does *Not* Do

- It is **not** a kernel module (by design)
- It does **not** rely on post-mount scanning
- It does **not** trust user-space tooling to enforce access
- It does **not** attempt to replace full endpoint protection solutions

GuardMount is focused on **early access control**, not broad malware detection.

---

## Core Features

✅ **Early Device Interception via udev**

✅ **Default-Deny Policy for External Peripherals**

✅ **Auto-Mount Prevention**

✅ **Protection Against HID / BadUSB-Class Attacks**

✅ **Explicit User Authorization Before Access**

✅ **Deterministic Enforcement Logic (Minimal Attack Surface)**

✅ **systemd Integration for Persistent Monitoring**

✅ **Security-First, Failure-Safe Design**

---

## Project Status

🚧 **Active Rebuild / Learning-Oriented Refactor**

GuardMount is currently being **restructured from the ground up** with a strong focus on:

- C-based systems programming
- Linux internals (udev, systemd, device handling)
- Secure design principles
- Clear separation of enforcement and policy

This project doubles as a **learning platform for kernel-adjacent security engineering**, not just a finished tool.

---

## Disclaimer

GuardMount is a **security research and learning project**.
It should be reviewed, tested, and adapted before use in production environments.

---

## Author

**RedKernel**
Offensive Security • Linux Internals • Kernel-Adjacent Engineering

