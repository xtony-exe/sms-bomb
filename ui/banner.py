from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box
import time

def show_banner(console: Console, theme: dict):
    banner_lines = [
        " ███████ ███    ███ ███████     ██████   ██████  ███    ███ ██████  ",
        " ██      ████  ████ ██          ██   ██ ██    ██ ████  ████ ██   ██ ",
        " ███████ ██ ████ ██ ███████     ██████  ██    ██ ██ ████ ██ ██████  ",
        "      ██ ██  ██  ██      ██     ██   ██ ██    ██ ██  ██  ██ ██   ██ ",
        " ███████ ██      ██ ███████     ██████   ██████  ██      ██ ██████  ",
    ]
    
    colors = [theme["primary"], theme["secondary"], theme["primary"], theme["secondary"], theme["accent"]]
    styled_banner = ""
    for i, line in enumerate(banner_lines):
        styled_banner += f"[{colors[i % len(colors)]}]{line}[/]\n"
    
    dev_text = Text()
    dev_text.append("Developer: ", style=theme["primary"])
    dev_text.append("xtony.exe", style=f"{theme['success']} bold")
    dev_text.append(" | Version: ", style=theme["primary"])
    dev_text.append("3.0", style=f"{theme['accent']} bold")
    dev_text.append(" | Status: ", style=theme["primary"])
    dev_text.append("✓ ELITE", style=f"{theme['success']} bold")
    
    panel = Panel(
        Align.center(styled_banner.strip()),
        subtitle=dev_text,
        border_style=theme["border"],
        box=box.DOUBLE,
        padding=(1, 2)
    )
    
    console.print()
    console.print(panel)
    console.print(Align.center(f"[{theme['secondary']} dim]Advanced SMS Bombing Framework for Sri Lanka[/]"))
    console.print()
