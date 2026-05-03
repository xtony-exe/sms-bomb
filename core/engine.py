import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Any, Callable
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.console import Console

from core.base import BaseBomber, get_shutdown_flag, set_shutdown_flag, set_interrupted_flag

class AttackEngine:
    def __init__(self, console: Console):
        self.console = console
        self.start_time = 0
        self.results = []

    def run(self, bombers: List[BaseBomber], num_msgs_per: List[int], delay: float) -> List[Tuple[int, int]]:
        self.start_time = time.time()
        self.results = []
        
        # Reset shutdown flags
        set_shutdown_flag(False)
        set_interrupted_flag(False)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.console,
            refresh_per_second=10,
        ) as progress:
            
            tasks = []
            for i, bomber in enumerate(bombers):
                tid = progress.add_task(
                    f"[{bomber.color}]Initializing {bomber.service_name}...", 
                    total=num_msgs_per[i]
                )
                tasks.append((bomber, num_msgs_per[i], tid))
            
            # Use max 4 workers or number of bombers
            max_workers = min(len(bombers), 4)
            if max_workers == 0: return []

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(b.attack, m, delay, progress, t): (b, m)
                    for b, m, t in tasks
                }
                
                # Wait for all to complete or interrupt
                while any(f.running() for f in futures):
                    if get_shutdown_flag():
                        # We don't cancel futures here to allow graceful exit from loops
                        break
                    time.sleep(0.5)
                
                for future in as_completed(futures):
                    try:
                        self.results.append(future.result(timeout=5))
                    except Exception as e:
                        # self.console.print(f"[red]Error in service: {e}[/]")
                        self.results.append((0, 0))
            
            # Ensure results length matches bombers
            while len(self.results) < len(bombers):
                self.results.append((0, 0))

        return self.results

    def get_elapsed_time(self) -> float:
        return time.time() - self.start_time
