from dataclasses import dataclass
from datetime import datetime

@dataclass
class TimeResponse:
    hour: int
    minute: int

    def format_time(self) -> str:
        """Formatea la hora de manera amigable"""
        return f"Son las {self.hour}:{str(self.minute).zfill(2)}"


class GetTimeUseCase:
    def execute(self) -> TimeResponse:
        now = datetime.now()
        return TimeResponse(
            hour=now.hour,
            minute=now.minute
        )
