# AI Citation: I built the heuristic monitoring logic and risk scoring.
# I utilized an AI assistant (Gemini/ChatGPT/Deepseek) to optimize the OS calls using 
# lazy evaluation, refine the regex patterns, and improve the formatting.

import psutil
import time
import os
import json
import re
from typing import Tuple, List, Dict, Optional
from datetime import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

class EDRSimulator:
    """
    Heuristic EDR Simulator. Monitors process behaviors, file handles, 
    and incorporates alert caching and JSON persistence.
    """
    def __init__(self):
        self.my_pid = os.getpid() 
        
        # Regex for signature matching and obfuscation detection
        self.SUSPICIOUS_REGEX = re.compile(
            r'(auditor\.py|keylog(?:ger)?|pynput|pyxhook|cryptography|fernet|pyarmor|pyinstaller|base64\.b64decode|exec\()', 
            re.IGNORECASE
        )
        
        self.TARGET_FILES = {'secret.key', 'encrypted_audit.log'}
        self.SCAN_INTERVAL = 5
        self.WHITELIST = {'taskmgr.exe', 'explorer.exe', 'system idle process'}
        
        if os.name == 'nt':
            self.SUSPICIOUS_PATHS = ['appdata', 'temp', 'public'] 
        else:
            self.SUSPICIOUS_PATHS = ['/tmp', '/var/tmp', '/dev/shm']
        
        self.alert_cache: Dict[int, float] = {} 
        self.alert_cooldown = 60
        self.loop_iterations = 0 
        self.json_log = "edr_alerts.json"

    def calculate_risk(self, p_info: dict, proc: Optional[psutil.Process] = None) -> Tuple[int, List[str]]:
        """Analyzes process telemetry. Uses lazy evaluation on `proc` to save CPU cycles."""
        score = 0
        findings = []
        
        cmdline_list = p_info.get('cmdline')
        if not cmdline_list:
            return score, findings
        
        cmdline = " ".join(cmdline_list).lower()
        exe_path = p_info.get('exe', '').lower() if p_info.get('exe') else ""

        # 1. Behavioral Regex Analysis
        if self.SUSPICIOUS_REGEX.search(cmdline):
            score += 60 
            findings.append("Suspicious Process Signature/Obfuscator Detected")

        # 2. Open Handle Analysis (Lazy Evaluation)
        if proc:
            try:
                open_files = proc.open_files()
                if open_files:
                    basenames = {os.path.basename(f.path).lower() for f in open_files}
                    if basenames & self.TARGET_FILES:
                        score += 50
                        findings.append("Active Handle on Audit Artifacts")
            except (psutil.AccessDenied, psutil.NoSuchProcess, AttributeError):
                pass

        # 3. Execution Path Checking
        if any(path in exe_path for path in self.SUSPICIOUS_PATHS):
            score += 20
            findings.append("Execution from Volatile Directory")

        # 4. Parent Tree Structure
        if proc:
            try:
                parent = proc.parent()
                if parent and parent.name().lower() in ['cmd.exe', 'powershell.exe', 'bash', 'zsh']:
                    score += 10
                    findings.append("Shell-Spawned Process")
            except Exception: 
                pass

        return min(score, 100), findings 

    def log_alert(self, p_info: dict, score: int, findings: List[str]) -> None:
        """Saves alerts to a Standard JSON Array and prints to console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_alert = {
            "timestamp": timestamp,
            "pid": p_info['pid'],
            "name": p_info['name'],
            "user": p_info.get('username', 'N/A'),
            "confidence": score,
            "indicators": findings,
            "command": " ".join(p_info['cmdline'])
        }

        alerts_list = []
        if os.path.exists(self.json_log):
            try:
                with open(self.json_log, "r") as f:
                    alerts_list = json.load(f)
            except (json.JSONDecodeError, IOError):
                alerts_list = []

        alerts_list.append(new_alert)

        try:
            with open(self.json_log, "w") as f:
                json.dump(alerts_list, f, indent=4)
        except Exception as e:
            print(f"{Fore.RED}[!] Error writing to JSON log: {e}")

        if score >= 80:
            header = f"{Back.RED}{Fore.WHITE}{Style.BRIGHT} CRITICAL ALERT "
            txt_color = Fore.RED
        else:
            header = f"{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT} WARNING ALERT "
            txt_color = Fore.YELLOW
        
        print(f"\n{header}")
        print(f"{txt_color}    TIME:      {timestamp}")
        print(f"{txt_color}    ENTITY:    {p_info['name']} (PID: {p_info['pid']})")
        print(f"{txt_color}    USER:      {p_info.get('username', 'N/A')}")
        print(f"{txt_color}    CONFIDENCE: {score}%")
        print(f"{txt_color}    INDICATORS: {', '.join(findings)}")
        print(f"{Fore.WHITE}    COMMAND:   {' '.join(p_info['cmdline'])}")
        print(f"{Style.DIM}" + "-" * 65)

    def monitor(self) -> None:
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "="*65)
        print(f"{Fore.CYAN}[*] EDR SIMULATOR PRO | STATUS: {Fore.GREEN}MONITORING")
        print(f"{Fore.CYAN}[*] JSON Logging: {Fore.WHITE}Standard Array Mode")
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "="*65 + "\n")

        try:
            while True:
                found_threat = False
                current_time = time.time()

                for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username', 'exe']):
                    try:
                        p_info = proc.info
                        if p_info['pid'] == self.my_pid or not p_info['cmdline'] or p_info['name'].lower() in self.WHITELIST:
                            continue

                        score, findings = self.calculate_risk(p_info, proc)

                        if score >= 50:
                            pid = p_info['pid']
                            if pid not in self.alert_cache or (current_time - self.alert_cache[pid]) > self.alert_cooldown:
                                self.log_alert(p_info, score, findings)
                                self.alert_cache[pid] = current_time
                                found_threat = True

                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                self.loop_iterations += 1
                if self.loop_iterations % 100 == 0:
                    self.alert_cache = {
                        pid: ts for pid, ts in self.alert_cache.items() 
                        if current_time - ts <= self.alert_cooldown
                    }

                if not found_threat:
                    status_time = datetime.now().strftime('%H:%M:%S')
                    print(f"{Fore.BLUE}[{status_time}] {Fore.GREEN}Threat Level: Normal", end="\r")

                time.sleep(self.SCAN_INTERVAL)
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.RED}[+] EDR Session Terminated by Administrator.")

if __name__ == "__main__":
    detector = EDRSimulator()
    detector.monitor()