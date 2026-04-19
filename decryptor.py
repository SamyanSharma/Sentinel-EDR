# AI Citation: I designed the core decryption flow and file handling.
# I utilized an AI assistant (Gemini/ChatGPT/Deepseek) to add type hinting, refine the
# HMAC exception handling, and format the JSON summary export.

import os
import argparse
import json
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken

def decrypt_logs(log_file: str, output_file: str, key_file: str, verbose: bool, json_summary: str) -> None:
    """
    Forensic CLI utility for decrypting binary audit logs.
    Includes built-in HMAC integrity checking and SIEM-compatible JSON reporting.
    """
    if not os.path.exists(key_file):
        print(f"[!] Error: Key file '{key_file}' not found.")
        return

    if not os.path.exists(log_file):
        print(f"[!] Error: Encrypted log '{log_file}' not found.")
        return
    
    with open(key_file, "rb") as f:
        key = f.read()

    cipher = Fernet(key)
    print(f"[*] Decrypting {log_file}...")

    try:
        with open(log_file, "rb") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
            valid_blocks = 0
            corrupt_blocks = 0  
            
            for line_num, line in enumerate(f_in, start=1):
                clean_line = line.rstrip(b'\n')
                if clean_line:
                    try:
                        decrypted_data = cipher.decrypt(clean_line).decode()
                        f_out.write(decrypted_data)
                        valid_blocks += 1
                        
                        if verbose and valid_blocks % 50 == 0:
                            print(f"[*] Decrypted {valid_blocks} blocks...")
                            
                    except InvalidToken:
                        corrupt_blocks += 1
                        error_msg = f"\n[!] DATA INTEGRITY ERROR: Line {line_num} tampered or corrupt.\n"
                        f_out.write(error_msg)
                        if verbose: print(error_msg.strip())
                    except Exception as e:
                        corrupt_blocks += 1
                        f_out.write(f"\n[!] DECRYPTION ERROR on line {line_num}: {e}\n")
            
            f_out.write("\n")
                        
        print(f"\n[+] Success! {valid_blocks} blocks securely decrypted.")
        if corrupt_blocks > 0:
            print(f"[-] WARNING: {corrupt_blocks} blocks were corrupt and skipped.")
        print(f"[+] Plaintext saved to: {os.path.abspath(output_file)}")

        if json_summary:
            summary = {
                "timestamp": datetime.now().isoformat(),
                "log_file": log_file,
                "total_blocks_processed": valid_blocks + corrupt_blocks,
                "valid_blocks": valid_blocks,
                "corrupt_blocks": corrupt_blocks,
                "success_rate": round(valid_blocks / max(1, (valid_blocks + corrupt_blocks)) * 100, 2)
            }
            with open(json_summary, "w") as jf:
                json.dump(summary, jf, indent=4)
            print(f"[+] Forensic summary exported to: {json_summary}")

    except Exception as e:
        print(f"[!] Fatal Error during file processing: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EDR Simulation - Forensic Decryption Utility")
    parser.add_argument("--log", default="encrypted_audit.log", help="Target encrypted log file")
    parser.add_argument("--output", default="decrypted_audit.txt", help="Output plaintext destination")
    parser.add_argument("--key", default="secret.key", help="Decryption key file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--json-summary", default="", help="Export a JSON forensic summary to this path")
    
    args = parser.parse_args()
    decrypt_logs(args.log, args.output, args.key, args.verbose, args.json_summary)