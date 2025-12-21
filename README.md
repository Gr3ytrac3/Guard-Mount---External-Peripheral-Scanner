---

![Process Diagram](https://github.com/Gr3ytrac3/Guard-Mount---External-Peripheral-Scanner/blob/b5dbbb53f08e5192246df2ff8e7643b0ae4676ab/guard-mount.png)

<h1 align="center">
  🛡️ GuardMount (Building Phase)
</h1>
<h4 align="center">
  Kernel-Level External Device Interception & Threat Gatekeeper for Linux
</h4>

<p align="center">
  <code>RedKernel</code> • <code>Kernel Security</code> • <code>Pre-Mount Threat Interception</code> • <code>Advanced Red Team Defense</code>
</p>

---

## What is GuardMount?

**GuardMount** is a next-generation Linux security tool that intercepts all external peripheral devices (USBs, HDDs, BadUSB devices) **at the kernel level before they can mount**, scans their content for malicious payloads, and **requires explicit user authorization to proceed**.

Unlike traditional USB scanners that react **after** the device mounts, **GuardMount acts as a gatekeeper, blocking auto-mount events through custom UDEV rules**. It ensures that no device touches your filesystem without passing an in-depth threat analysis — effectively eliminating split-second payload execution vectors.

---

## Why Pre-Mount Interception Matters

Modern attack vectors (BadUSB, Rubber Ducky payloads, autorun scripts) can exploit devices **the moment they are mounted**. A fraction of a second is enough to:

* Trigger silent autorun scripts
* Inject malicious HID commands
* Execute stealthy firmware payloads

GuardMount stops this by:

* **Intercepting kernel mount events (via UDEV control)**
* Scanning the device **before** the system interacts with it
* Giving you the final say to allow, deny, or quarantine the device

---

## Core Features

✅ **Kernel-Level Device Interception (UDEV Rule Integration)**

✅ **Blocks Auto-Mount Until Scan & Authorization**

✅ **Rubber Ducky & HID Attack Prevention**

✅ **Full Content Analysis using ClamAV + Heuristic Rules**

✅ **Persistent Device Fingerprinting (Serial, VID/PID Check)**

✅ **Terminal-Based Threat Report & User Prompt**

✅ **Mount Devices Only After Approval (Read-Only Mode by Default)**

✅ **Systemd Integration for Persistent Background Monitoring**


