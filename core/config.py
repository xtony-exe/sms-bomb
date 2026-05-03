import json
import os
from typing import Dict, Any

DEFAULT_CONFIG = {
    "default_phone": "712345678",
    "default_messages": 10,
    "default_delay": 1.0,
    "theme": "neon",
    "last_used_services": ["eChannelling", "SLT"],
    "proxy": {
        "enabled": False,
        "list": []
    }
}

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except Exception:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save_config()
