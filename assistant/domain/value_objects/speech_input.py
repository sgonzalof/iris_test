from dataclasses import dataclass

@dataclass(frozen=True)
class SpeechInput:
    """Raw speech input from user"""
    text: str
    confidence: float = 0.0

    def is_valid(self) -> bool:
        """Check if the speech input is valid"""
        return bool(self.text and self.text.strip())