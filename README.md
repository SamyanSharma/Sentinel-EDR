# 🛡️ Sentinel-EDR: Advanced Endpoint Detection & Auditing Suite
> A digital security guard for your PC that catches 'bad behavior' from apps and locks the evidence behind a secure vault.

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue) 
![License](https://img.shields.io/badge/license-MIT-green) 
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey) 
![Status](https://img.shields.io/badge/status-stable-brightgreen)

⭐ *If you found this project useful or educational, consider starring the repo!*

---

## 🚀 Overview
**Sentinel-EDR** is a tool that monitors your computer for suspicious activity, secures that data with encryption, and alerts you to potential threats. It shows how modern security software catches "red flags" to stop hackers in real-time.

👉 *This project demonstrates how security systems watch, encrypt, and analyze program behavior to keep a system safe.* [cite: 1]

### ⭐ Key Highlights
* **Smooth Performance:** Uses a smart "queue" system so the security monitoring doesn't slow down your typing. [cite: 1]
* **Bank-Grade Security:** Encrypts all captured data so only authorized users can read it. [cite: 1]
* **Smart Detection:** Uses pattern matching and system "heartbeat" checks to find hidden threats. [cite: 1]
* **Easy Reporting:** Creates simple summaries for security experts to review. [cite: 1]

---

## ⚠️ Ethical Disclaimer
**FOR EDUCATIONAL AND AUTHORIZED AUDITING ONLY.**
This software monitors computer activity. Using it to watch someone without their permission is illegal and strictly prohibited. This was built for learning and security research only. [cite: 1]

---

## 💼 Resume Highlights
* Built a high-performance system that processes data without lagging the computer. [cite: 1]
* Implemented AES-256 encryption to keep data private and tamper-proof. [cite: 1]
* Created a "detection engine" that finds threats based on how programs behave. [cite: 1]
* Developed tools to turn messy security data into readable forensic reports. [cite: 1]

---

## 🛠️ Tech Stack & Tools
* **Python 3.9+**
* [**pynput**](https://pypi.org/project/pynput/): To watch for keyboard activity. [cite: 1]
* [**cryptography**](https://cryptography.io/en/latest/): To lock and unlock the data vault. [cite: 1]
* [**psutil**](https://psutil.readthedocs.io/): To check what programs are doing on the system. [cite: 1]
* [**colorama**](https://pypi.org/project/colorama/): To make the security alerts easy to read. [cite: 1]

---

## 🧩 How It Works

```text
[What You Do]
       ↓
   The Auditor (Watches activity and encrypts it)
       ↓
   The Vault (A secure file where data is hidden)
       ↓
   The Decryptor (Unlocks the data)  ←  The Detector (The 'Brain' that finds threats)
       ↓                                       ↓
[Readable Report]                       [Real-time Alerts]
```

### 📁 What's Inside?
```text
sentinel-edr/
├── auditor.py          # The collector that watches and encrypts activity
├── decryptor.py        # The tool that unlocks and reads the logs
├── detector.py         # The 'brain' that scans for bad programs
├── requirements.txt    # List of tools needed to run the project
├── LICENSE             # The project's usage rules
└── README.md           # This document
```

---

## 📦 Main Components

### 🔹 The Auditor (`auditor.py`)
This is the "collector." It watches what happens and quickly hides that info in a secure vault.
* **No Lag:** It works in the background so you won't even know it's there. [cite: 1]
* **Clean Storage:** It automatically organizes its files so they don't take up too much space. [cite: 1]

### 🔹 The Decryptor (`decryptor.py`)
This is the "key." It allows a security pro to open the vault and see exactly what happened. [cite: 1]
* **Tamper Check:** It knows if someone tried to mess with the files and will warn you. [cite: 1]

### 🔹 The Detector (`detector.py`)
This is the "sentinel." It constantly scans your computer for programs acting like "red flags." [cite: 1]
* **Smart Scanning:** It only looks deep into a program if it sees something suspicious first, which saves battery and power. [cite: 1]

---

## 📸 Example Alert

<details>
<summary><b>See what a threat alert looks like</b></summary>

```text
CRITICAL ALERT 
    TIME:       2026-04-19 21:40:59
    ENTITY:     python.exe (PID: 26156)
    CONFIDENCE: 100% (High Risk!)
    REASON:     Suspicious behavior and unauthorized file access detected.
    COMMAND:    C:\Python313\python.exe auditor.py
-----------------------------------------------------------------
```
</details>

---

## 🧠 Smart Design Choices

<details>
<summary><b>1. Why use a background 'queue'?</b></summary>
Saving files is slow, but typing is fast. We use a "waiting room" (queue) for data so your computer stays fast while the security tool does its work. [cite: 1]
</details>

<details>
<summary><b>2. Why use 'Lazy' scanning?</b></summary>
Checking every single file on a computer is exhausting for the processor. Our tool only does a deep dive when it sees a suspicious "red flag" first. [cite: 1]
</details>

---

## ⚡ Quick Start (Try it yourself!)

**Prerequisites:** Python 3.9 or higher installed. [cite: 1]

1.  **Download and Setup:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/Sentinel-EDR.git
    cd Sentinel-EDR
    pip install -r requirements.txt
    ```

2.  **Run the Simulation:**
    Open three separate terminal windows.

    ```bash
    # Terminal 1: Start the Security Guard (The Detector)
    # (Note: Run as Administrator on Windows or use 'sudo' on Mac/Linux)
    python detector.py
    ```

    ```bash
    # Terminal 2: Start the Activity Collector (The Auditor)
    python auditor.py
    
    # After typing a few things, press 'Ctrl+C' here to stop.
    ```
    
    *As you type, Terminal 1 will show alerts if it catches the Collector acting suspiciously!*

    ```bash
    # Terminal 3: Unlock and read the logs
    python decryptor.py --log encrypted_audit.log --output report.txt
    ```

---

## 🤝 Status & Credits
* **Status:** Complete. This is a personal project and not looking for new updates. [cite: 1]
* **Credits:** Built for the Final Project of Harvard University's CS50x course. [cite: 1]

---

## 📄 License
Distributed under the MIT License. See [`LICENSE`](LICENSE) for details. [cite: 1]
