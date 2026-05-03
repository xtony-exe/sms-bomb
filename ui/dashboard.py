from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from core.utils import format_time

def show_final_stats(console: Console, bombers: list, results: list, elapsed: float, theme: dict):
    total_sent = sum(r[0] for r in results)
    total_failed = sum(r[1] for r in results)
    
    table = Table(title=f"📊 Attack Statistics", box=box.ROUNDED, border_style=theme["success"])
    table.add_column("Service", style=theme["primary"])
    table.add_column("Sent", justify="right", style=theme["success"])
    table.add_column("Failed", justify="right", style=theme["error"])
    table.add_column("Success Rate", justify="right")

    for i, bomber in enumerate(bombers):
        sent, failed = results[i]
        rate = (sent / (sent + failed) * 100) if (sent + failed) > 0 else 0
        table.add_row(
            bomber.service_name, 
            str(sent), 
            str(failed), 
            f"{rate:.1f}%"
        )
    
    console.print("\n")
    console.print(Align.center(table))
    
    summary_table = Table(show_header=False, box=box.SIMPLE, border_style=theme["accent"])
    summary_table.add_row("Total Sent:", f"[bold {theme['success']}]{total_sent}[/]")
    summary_table.add_row("Total Failed:", f"[bold {theme['error']}]{total_failed}[/]")
    summary_table.add_row("Time Elapsed:", format_time(elapsed))
    
    if total_sent > 0:
        rate = total_sent / elapsed if elapsed > 0 else 0
        summary_table.add_row("Overall Speed:", f"{rate:.1f} msgs/sec")

    console.print(Align.center(Panel(summary_table, title="Summary", border_style=theme["border"], width=40)))
    console.print("\n")
