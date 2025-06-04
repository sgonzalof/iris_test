from dataclasses import dataclass
from typing import List

@dataclass
class Iris:
    activation_phrases: List[str]
    
    def is_activated_by(self, phrase: str) -> bool:
        return any(trigger.lower() in phrase.lower() for trigger in self.activation_phrases)