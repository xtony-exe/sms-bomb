from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich.align import Align
from rich import box
from typing import Tuple, List

def main_menu(console: Console, theme: dict) -> str:
    table = Table(show_header=False, box=box.ROUNDED, border_style=theme["primary"])
    table.add_column("Option", style=theme["primary"], width=4)
    table.add_column("Description", style="white")
    
    table.add_row("[1]", f"[{theme['accent']}]Quick Attack (Default Services)[/]")
    table.add_row("[2]", f"[{theme['accent']}]Custom Attack (Select Services)[/]")
    table.add_row("[3]", f"[{theme['accent']}]Attack Profiles (Presets)[/]")
    table.add_row("[4]", f"[{theme['accent']}]Settings & Themes[/]")
    table.add_row("[5]", "[red]Exit[/]")
    
    panel = Panel(
        Align.center(table),
        title=f"[bold white]📋 MAIN MENU v3.0[/]",
        border_style=theme["border"],
        padding=(1, 2)
    )
    
    console.print(Align.center(panel))
    
    choice = Prompt.ask(
        f"\n[bold {theme['success']}]Select option[/]",
        choices=['1', '2', '3', '4', '5'],
        default='1',
        show_choices=False
    )
    
    return choice

def service_selection_menu(console: Console, all_services: List[str], theme: dict) -> List[str]:
    console.print(f"\n[bold {theme['primary']}]Select Services (comma separated numbers, or 'all'):[/]")
    for i, service in enumerate(all_services, 1):
        console.print(f"  [{theme['accent']}]{i}.[/] {service}")
    
    choice = Prompt.ask(f"\n[bold {theme['success']}]Selection[/]", default="all")
    if choice.lower() == 'all':
        return all_services
    
    try:
        indices = [int(x.strip()) - 1 for x in choice.split(',')]
        return [all_services[i] for i in indices if 0 <= i < len(all_services)]
    except Exception:
        return [all_services[0]]

def profile_menu(console: Console, theme: dict) -> Tuple[int, float, str]:
    table = Table(title="Attack Profiles", border_style=theme["primary"])
    table.add_column("Profile", style=theme["accent"])
    table.add_column("Messages", justify="right")
    table.add_column("Delay", justify="right")
    table.add_column("Service Load")

    table.add_row("Light", "10", "2.0s", "1 Service")
    table.add_row("Medium", "50", "1.0s", "2 Services")
    table.add_row("Heavy", "100", "0.5s", "All Services")
    table.add_row("Custom", "?", "?", "?")

    console.print(Align.center(table))
    
    choice = Prompt.ask(f"\n[bold {theme['success']}]Choose Profile[/]", choices=["Light", "Medium", "Heavy", "Custom"], default="Medium")
    
    if choice == "Light": return 10, 2.0, "Light"
    if choice == "Medium": return 50, 1.0, "Medium"
    if choice == "Heavy": return 100, 0.5, "Heavy"
    return 0, 0, "Custom"

def settings_menu(console: Console, current_theme: str, theme: dict) -> str:
    console.print(f"\n[bold {theme['primary']}]Settings:[/]")
    console.print(f"  Current Theme: [bold {theme['accent']}]{current_theme}[/]")
    
    new_theme = Prompt.ask(
        f"\n[bold {theme['success']}]Choose New Theme[/]",
        choices=["neon", "hacker", "stealth", "blood", "Back"],
        default="Back"
    )
    return new_theme
