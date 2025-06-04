from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Command:
    text: str
    intent: str
    parameters: dict[str, str]
    
    @property
    def is_valid(self) -> bool:
        return bool(self.text and self.intent)