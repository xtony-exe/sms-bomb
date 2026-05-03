from typing import List, Type
from core.base import BaseBomber

from services.echannelling import EChannellingBomber
from services.slt import SLTBomber

SERVICE_MAP = {
    "eChannelling": EChannellingBomber,
    "SLT": SLTBomber,
}

def get_all_services() -> List[str]:
    return list(SERVICE_MAP.keys())

def get_bomber_class(name: str) -> Type[BaseBomber]:
    return SERVICE_MAP.get(name)

def get_all_bomber_classes() -> List[Type[BaseBomber]]:
    return list(SERVICE_MAP.values())
