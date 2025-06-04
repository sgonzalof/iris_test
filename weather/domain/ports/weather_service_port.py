from abc import ABC, abstractmethod
from datetime import date
from ..value_objects.weather import Weather

class WeatherServicePort(ABC):
    @abstractmethod
    def get_weather(self, city: str, forecast_date: date) -> Weather:
        """Get weather information for a specific city and date"""
        pass