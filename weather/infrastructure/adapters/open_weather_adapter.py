import requests
from datetime import date
from ...domain.ports.weather_service_port import WeatherServicePort
from ...domain.value_objects.weather import Weather
from config import Config

class OpenWeatherAdapter(WeatherServicePort):
    def __init__(self, config: Config):
        self._api_key = config.WEATHER_API_KEY
        self._base_url = "http://api.openweathermap.org/data/2.5/forecast"
    
    def get_weather(self, city: str, forecast_date: date) -> Weather:
        try:
            params = {
                'q': city,
                'appid': self._api_key,
                'units': 'metric',
                'lang': 'es'
            }
            
            response = requests.get(self._base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Find forecast for requested date
            for forecast in data['list']:
                forecast_date_str = forecast['dt_txt'].split()[0]
                if date.fromisoformat(forecast_date_str) == forecast_date:
                    return Weather(
                        temperature=forecast['main']['temp'],
                        description=forecast['weather'][0]['description'],
                        city=data['city']['name'],
                        date=forecast_date,
                        humidity=forecast['main']['humidity']
                    )
                    
            raise ValueError(f"No forecast available for {forecast_date}")
            
        except requests.RequestException as e:
            raise RuntimeError(f"Error fetching weather data: {e}")