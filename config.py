from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Config:
    WEATHER_API_KEY: str = "8307a29631b931fb73f2475ab1f2e514"
    ACTIVATION_PHRASES: List[str] = field(
        default_factory=lambda: ["iris", "hey iris", "oye iris"]
    )
    DEFAULT_LANGUAGE: str = "es-ES"
    DEFAULT_MIC_INDEX: int = 1
    CONFIDENCE_THRESHOLD: float = 0.5
    DEBUG: bool = True