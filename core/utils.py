import random
import string
from typing import Tuple

def clean_phone_number(phone: str) -> str:
    """Extract the core 9-digit number from any format"""
    digits = ''.join(filter(str.isdigit, phone))
    return digits[-9:] if len(digits) >= 9 else digits

def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate Sri Lankan phone number"""
    clean = clean_phone_number(phone)
    if len(clean) == 9:
        return True, clean
    return False, "Phone number must be 9 digits (e.g., 712345678)"

def format_time(seconds: float) -> str:
    """Format time in seconds to readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{int(minutes)}m {int(secs)}s"

def random_user_agent() -> str:
    """Return a random modern user agent"""
    # Simple list for now, can be replaced by fake-useragent if desired
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    ]
    return random.choice(user_agents)

def generate_random_string(length: int = 8) -> str:
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_name() -> str:
    """Generate random name"""
    first_names = ["Dulith", "Kamal", "Nimal", "Sunil", "Priya", "Ruwan", "Tharindu", "Lakshitha", "Nuwan", "Kasun", "Amila", "Ishara", "Janith", "Madush", "Prageeth"]
    last_names = ["Perera", "Fernando", "Silva", "Bandara", "Kumara", "Senanayake", "Jayasinghe", "Herath", "Gunawardena", "Rathnayake"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_email() -> str:
    """Generate random email address"""
    domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com"]
    return f"{generate_random_string(10).lower()}@{random.choice(domains)}"
