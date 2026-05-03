THEMES = {
    "neon": {
        "banner": "bold cyan",
        "primary": "cyan",
        "secondary": "magenta",
        "accent": "yellow",
        "success": "green",
        "error": "red",
        "border": "bold cyan"
    },
    "hacker": {
        "banner": "bold green",
        "primary": "green",
        "secondary": "bright_green",
        "accent": "white",
        "success": "bold green",
        "error": "red",
        "border": "green"
    },
    "stealth": {
        "banner": "bold white",
        "primary": "white",
        "secondary": "grey70",
        "accent": "grey100",
        "success": "white",
        "error": "grey37",
        "border": "bold white"
    },
    "blood": {
        "banner": "bold red",
        "primary": "red",
        "secondary": "dark_red",
        "accent": "white",
        "success": "green",
        "error": "bold red",
        "border": "bold red"
    }
}

def get_theme(name: str):
    return THEMES.get(name, THEMES["neon"])
