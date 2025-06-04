from dataclasses import dataclass

@dataclass(frozen=True)
class SpeechOutput:
    """Text to be converted to speech"""
    text: str
    language: str = "es-ES"
    speed: float = 1.3