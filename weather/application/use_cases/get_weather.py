from dataclasses import dataclass
from datetime import date
from ...domain.ports.weather_service_port import WeatherServicePort


@dataclass
class GetWeatherRequest:
    city: str
    forecast_date: date
    

class GetWeatherUseCase:
    def __init__(self, weather_service: WeatherServicePort):
        self._weather_service = weather_service
    
    def execute(self, request: GetWeatherRequest) -> str:
        try:
            weather = self._weather_service.get_weather(
                request.city, 
                request.forecast_date
            )
            return weather.format_response()
        except Exception as e:
            return f"Lo siento, no pude obtener el pronóstico: {str(e)}"