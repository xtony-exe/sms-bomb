#!/usr/bin/env python3
"""
SMS BOMB v3.0 - Full Update
Developer: xtony.exe
Modular Architecture Edition
"""

import sys
import time
import signal
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm

# Import core
from core.config import ConfigManager
from core.engine import AttackEngine
from core.utils import validate_phone
from core.base import set_shutdown_flag, set_interrupted_flag, get_shutdown_flag

# Import services
from services import get_all_services, get_bomber_class

# Import UI
from ui.themes import get_theme
from ui.banner import show_banner
from ui.menu import main_menu, service_selection_menu, profile_menu, settings_menu
from ui.dashboard import show_final_stats

console = Console()
config = ConfigManager()

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    if not get_shutdown_flag():
        console.print("\n\n[bold yellow]⚠️ Interrupt received! Shutting down gracefully...[/]")
        set_shutdown_flag(True)
        set_interrupted_flag(True)
    else:
        console.print("\n[bold red]Force quitting...[/]")
        sys.exit(1)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

def run_attack_flow(selected_services: list, phone: str, num_msgs: int, delay: float):
    theme = get_theme(config.get("theme"))
    
    bombers = []
    for sname in selected_services:
        cls = get_bomber_class(sname)
        if cls:
            bombers.append(cls(phone))
    
    if not bombers:
        console.print("[bold red]No valid services selected![/]")
        return

    # Split messages across services
    msgs_per = []
    base_msgs = num_msgs // len(bombers)
    remainder = num_msgs % len(bombers)
    for i in range(len(bombers)):
        msgs_per.append(base_msgs + (1 if i < remainder else 0))

    engine = AttackEngine(console)
    
    console.print(f"\n[bold {theme['primary']}]🚀 Target Locked:[/]")
    console.print(f"  📱 Phone: [bold {theme['accent']}]{phone}[/]")
    console.print(f"  📨 Total Messages: [bold {theme['accent']}]{num_msgs}[/]")
    console.print(f"  🎯 Services: [bold {theme['accent']}]{', '.join(selected_services)}[/]")
    
    if not Confirm.ask(f"\n[bold {theme['success']}]Initiate Attack?[/]", default=True):
        return

    results = engine.run(bombers, msgs_per, delay)
    elapsed = engine.get_elapsed_time()
    
    show_final_stats(console, bombers, results, elapsed, theme)
    
    if not get_shutdown_flag():
        Prompt.ask(f"[dim]Press Enter to return to menu[/]")

def main():
    while True:
        try:
            theme_name = config.get("theme")
            theme = get_theme(theme_name)
            console.clear()
            show_banner(console, theme)
            
            choice = main_menu(console, theme)
            
            if choice == '5':
                console.print(f"\n[bold {theme['secondary']}]Goodbye! Stay Elite.[/]")
                break
            
            if choice == '4':
                new_theme = settings_menu(console, theme_name, theme)
                if new_theme != "Back":
                    config.set("theme", new_theme)
                continue

            # Target selection
            phone = Prompt.ask(f"[bold {theme['accent']}]📱 Target Phone (e.g. 712345678)[/]", default=config.get("default_phone"))
            valid, phone = validate_phone(phone)
            if not valid:
                console.print(f"[bold red]❌ {phone}[/]")
                time.sleep(1.5)
                continue
            config.set("default_phone", phone)

            num_msgs = config.get("default_messages")
            delay = config.get("default_delay")
            selected_services = config.get("last_used_services")

            if choice == '1': # Quick Attack
                pass 
            elif choice == '2': # Custom
                selected_services = service_selection_menu(console, get_all_services(), theme)
                config.set("last_used_services", selected_services)
                num_msgs = IntPrompt.ask(f"[bold {theme['accent']}]📨 Message Count[/]", default=num_msgs)
                delay = FloatPrompt.ask(f"[bold {theme['accent']}]⏱️  Delay (s)[/]", default=delay)
            elif choice == '3': # Profiles
                p_msgs, p_delay, p_name = profile_menu(console, theme)
                if p_name == "Custom":
                    continue
                num_msgs = p_msgs
                delay = p_delay
                if p_name == "Heavy":
                    selected_services = get_all_services()
                elif p_name == "Light":
                    selected_services = ["eChannelling"]
                else:
                    selected_services = ["eChannelling", "SLT"]

            run_attack_flow(selected_services, phone, num_msgs, delay)
            
            # Reset shutdown flags for next loop
            set_shutdown_flag(False)
            set_interrupted_flag(False)

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/]")
            time.sleep(2)

if __name__ == "__main__":
    main()