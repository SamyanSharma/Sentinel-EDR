# 🛡️ Sentinel-EDR: Advanced Endpoint Detection & Auditing Suite
> Built with Python | Multi-threaded | Secure logging | Heuristic detection

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Status](https://img.shields.io/badge/status-stable-brightgreen)

### 🎥 Video Demo: https://www.youtube.com/watch?v=wNZo4s3g54o

---

## 🚀 Overview
**Sentinel-EDR** is a lightweight Endpoint Detection & Response (EDR) framework that simulates real-world attack detection using encrypted telemetry, behavioral analysis, and heuristic scoring. Developed as a final project for **Harvard University's CS50x**, this suite bridges the gap between offensive auditing techniques and defensive security engineering.

👉 *This project demonstrates how modern EDR systems detect malicious behavior through a combination of telemetry collection, encryption, and heuristic analysis.*

### ⭐ Key Highlights
* **Producer–Consumer Architecture:** Utilizes a non-blocking multithreaded I/O pipeline for real-time input processing.
* **Cryptographic Integrity:** AES-256 (Fernet) encryption with HMAC tampering detection.
* **Heuristic Logic:** Regex-based signature matching combined with lazy-evaluation OS telemetry.
* **Forensic Reporting:** Generates SIEM-compatible JSON summaries for incident response.

---

## ⚠️ Ethical Disclaimer
**FOR EDUCATIONAL AND AUTHORIZED AUDITING ONLY.**
This software captures keystrokes and monitors system processes. Capturing data without explicit, documented user consent is strictly prohibited and potentially illegal. This project was developed solely for the purpose of studying defensive programming and heuristic analysis.

---

## 💼 What I Learned
* Designed a multi-threaded producer-consumer system for real-time input processing.
* Implemented AES-256 encryption with integrity verification (HMAC).
* Built a heuristic EDR engine with regex-based detection and OS-level telemetry.
* Developed SIEM-compatible forensic reporting tools.
* Leveraged O(min(n, m)) set intersection and lazy evaluation to significantly reduce monitoring overhead.

---

## 🛠️ Tech Stack & Tools
* **Python 3.9+**
* [**pynput**](https://pypi.org/project/pynput/): For cross-platform hardware input hooking.
* [**cryptography**](https://cryptography.io/en/latest/): Providing the Fernet (AES-256 + HMAC) cryptographic primitives.
* [**psutil**](https://psutil.readthedocs.io/): For deep operating system telemetry and process analysis.
* [**colorama**](https://pypi.org/project/colorama/): For rendering the terminal-based SOC dashboard.

---

## 🧩 System Architecture

```text
[Keyboard Input]
       ↓
   Auditor (Collector: auditor.py)
       ↓ (Encrypted Logs: AES-256)
   Storage (File System: encrypted_audit.log)
       ↓
   Decryptor (Forensics: decryptor.py)  ←  Detector (Sentinel: detector.py)
       ↓                                       ↓
[Plaintext Report]                      [Real-time Alerts]
```

### 📁 Repository Structure
```text
sentinel-edr/
├── auditor.py          # AES‑256 encrypted input auditor (producer‑consumer)
├── decryptor.py        # Forensic decryption tool
├── detector.py         # Heuristic EDR engine
├── requirements.txt    # Pinned dependency list
├── LICENSE             # MIT License
└── README.md           # Project documentation
```

---

## 📦 Components

### 🔹 The Auditor (`auditor.py`)
The "Collector" agent. It utilizes a producer-consumer multithreading model to ensure zero input lag.
* **Incremental Byte Tracking:** Efficiently monitors buffer size in O(1) time by maintaining a running byte counter, avoiding a full buffer re-scan on every keystroke.
* **Resilient I/O:** Background worker with a `queue.Queue` prevents disk lag during high-speed typing.
* **Log Rotation:** Automatically archives logs at 5MB intervals to prevent storage exhaustion.

### 🔹 The Decryptor (`decryptor.py`)
The "Forensic" tool. Used for post-incident data recovery and integrity verification.
* **HMAC Validation:** Detects if logs were tampered with using authentication tags.
* **JSON Summaries:** Exports automated forensic reports detailing success/corruption rates for SIEM ingestion.

### 🔹 The Detector (`detector.py`)
The "Sentinel" engine. A heuristic EDR that monitors the OS process table for Indicators of Compromise (IoC).
* **Lazy Evaluation:** Fetches expensive OS telemetry (file handles/parent trees) only when necessary based on initial risk.
* **Alert Caching:** Prevents alert fatigue by deduplicating alerts for 60 seconds per PID.

---

## 📸 Example Output

<details>
<summary><b>View Sample EDR Alert</b></summary>

```text
CRITICAL ALERT
    TIME:       2026-04-19 21:40:59
    ENTITY:     python.exe (PID: 26156)
    USER:       user
    CONFIDENCE: 100%
    INDICATORS: Suspicious Process Signature/Obfuscator Detected, Active Handle on Audit Artifacts
    COMMAND:    C:\Python313\python.exe auditor.py
-----------------------------------------------------------------
```
</details>

---

## 🧠 Design Decisions

<details>
<summary><b>1. Why a Producer-Consumer Model?</b></summary>
Writing to disk is slow; hardware input is fast. To prevent "keyboard lag," I decoupled these using a thread-safe Queue. The listener "produces" characters, and a background worker thread "consumes" and encrypts them.
</details>

<details>
<summary><b>2. Why Lazy Evaluation for OS Telemetry?</b></summary>
Calling `proc.open_files()` on every process every 5 seconds is incredibly CPU-intensive. Sentinel-EDR scans lightweight strings (regex against command-line arguments) first. It only performs the expensive OS-level forensics if the initial string risk score warrants further investigation.
</details>

<details>
<summary><b>3. Why Set Intersection for Detection?</b></summary>
Comparing raw lists requires a nested loop, which is an $O(N^2)$ operation. By converting our target files and the process's open file handles to Python sets, membership lookup drops from $O(N)$ per check to an average of $O(1)$. This allows the set intersection operator (`&`) to run in $O(\min(n, m))$ time, avoiding the $O(N^2)$ nested comparison trap and significantly reducing EDR overhead during the 5-second monitoring loop.
</details>

---

## ⚡ Quick Start & Installation

**Prerequisites:** Python 3.9 or higher.

1.  **Clone and Install:**
    ```bash
    git clone https://github.com/SamyanSharma/Sentinel-EDR.git
    cd Sentinel-EDR
    pip install -r requirements.txt
    ```

2.  **Simulate the Attack & Defense Environment:**
    Open three separate terminals.

    ```bash
    # Terminal 1 (Defense): Start the Sentinel EDR Engine
    # Note: On Linux/macOS, use `sudo python detector.py`. On Windows, run terminal as Administrator.
    python detector.py
    ```

    ```bash
    # Terminal 2 (Offense): Start the Auditor to simulate monitored activity
    python auditor.py

    # After typing, simply Kill/Close the Terminal 2 window. Due to the global nature of hardware hooks in virtualized environments (like VS Code), standard signals like Ctrl+C may be suppressed
    ```

    *Type a few keystrokes before stopping the Auditor. You will instantly see the Detector in Terminal 1 flag the Auditor based on its Regex signature and active file handles.*

    ```bash
    # Terminal 3 (Forensics): Decrypt the logs after stopping the Auditor
    python decryptor.py --log encrypted_audit.log --output decrypted_audit.txt --json-summary summary.json
    ```

---

## 🚧 Limitations & Roadmap
* **Current Limit:** Detection is primarily signature and regex-based, which can be bypassed by advanced in-memory obfuscation.
* **Future Goal:** Implement YARA rule integration for industry-standard signature matching.
* **Future Goal:** Add network telemetry scanning to detect data exfiltration (C2) attempts.

---

## 🤝 Contributing & Status
* **Status:** Stable. Maintained strictly for educational purposes and portfolio demonstration.
* **Contributing:** This repository is maintained as an academic portfolio piece. Issues and feedback are welcome, but PRs are not expected.
* **Acknowledgments:** This project was built as the Final Project for Harvard University's CS50x.

---

## 📄 License
Distributed under the MIT License. See [`LICENSE`](LICENSE) file for details.
