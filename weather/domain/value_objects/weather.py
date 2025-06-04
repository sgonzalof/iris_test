from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Weather:
    temperature: float
    description: str
    city: str
    date: date
    humidity: int
    
    def format_response(self) -> str:
        """Formats weather information into a natural language response"""
        return (
            f"El tiempo en {self.city} será de {int(self.temperature)} grados, "
            f"con {self.description} y {self.humidity}% de humedad"
        )