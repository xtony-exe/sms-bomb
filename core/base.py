import threading
import requests
import time
from typing import Tuple, List, Optional
from rich.progress import Progress
from core.utils import clean_phone_number, random_user_agent

# ============================================================================
# GLOBAL FLAGS FOR CLEAN SHUTDOWN
# ============================================================================
_SHUTDOWN_FLAG = False
_INTERRUPTED_FLAG = False
_FLAG_LOCK = threading.Lock()

def set_shutdown_flag(value: bool):
    with _FLAG_LOCK:
        global _SHUTDOWN_FLAG
        _SHUTDOWN_FLAG = value

def get_shutdown_flag() -> bool:
    with _FLAG_LOCK:
        return _SHUTDOWN_FLAG

def set_interrupted_flag(value: bool):
    with _FLAG_LOCK:
        global _INTERRUPTED_FLAG
        _INTERRUPTED_FLAG = value

def get_interrupted_flag() -> bool:
    with _FLAG_LOCK:
        return _INTERRUPTED_FLAG

# ============================================================================
# BASE BOMBER CLASS
# ============================================================================

class BaseBomber:
    def __init__(self, phone_number: str):
        self.phone = phone_number
        self.clean_number = clean_phone_number(phone_number)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": random_user_agent(),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        })
        self.sent_count = 0
        self.failed_count = 0
        self.service_name = "Base"
        self.color = "white"

    def check_running(self) -> bool:
        """Check if we should continue running"""
        return not get_shutdown_flag()

    def send_one(self, **kwargs) -> bool:
        """Implementation of sending a single request. Must return True/False."""
        raise NotImplementedError("Subclasses must implement send_one()")

    def ping(self) -> bool:
        """Health check to see if the service is alive"""
        return True

    def attack(self, num_msgs: int, delay: float, progress: Progress, task_id) -> Tuple[int, int]:
        """Generic attack loop. Subclasses can override if they need special logic."""
        sent = 0
        failed = 0
        
        progress.update(task_id, description=f"[{self.color}]{self.service_name}: Starting...")
        
        for i in range(num_msgs):
            if not self.check_running():
                break
            
            # Rotate user agent occasionally
            if i % 5 == 0:
                self.session.headers.update({"User-Agent": random_user_agent()})

            if self.send_one():
                sent += 1
                self.sent_count += 1
                progress.update(
                    task_id, 
                    advance=1,
                    description=f"[{self.color}]{self.service_name}: [green]✓ Sent {sent}/{num_msgs}"
                )
            else:
                failed += 1
                self.failed_count += 1
                progress.update(
                    task_id,
                    description=f"[{self.color}]{self.service_name}: [red]✗ Failed ({failed})"
                )
            
            if i < num_msgs - 1 and self.check_running():
                # Interruptible sleep
                for _ in range(int(delay * 10)):
                    if not self.check_running():
                        break
                    time.sleep(0.1)
        
        return sent, failed
