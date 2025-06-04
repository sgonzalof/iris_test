from datetime import date
import re
from typing import Dict, Tuple
from ...domain.ports.command_processor_port import CommandProcessorPort
from ...domain.value_objects.speech_input import SpeechInput
from ...domain.value_objects.comand import Command

class CommandProcessorAdapter(CommandProcessorPort):
    def __init__(self):
        self._command_patterns = {
            r"(?:busca|reproduce|pon).*?(?:en )?youtube ([\w\s]+)": ("youtube", lambda m: {"query": m.group(1).strip()}),
            r"busca.*?(?:en )?google ([\w\s]+)": ("google", lambda m: {"query": m.group(1).strip()}),
            r"(?:qué|dime)?.*?(?:hora|hora es).*?": lambda m: ("time", {}),
            r"(?:qué )?tiempo.*?(?:en|de) ([\w\s]+?)(?:\s+(?:el|para el)\s+(\d{1,2})(?:\s+de\s+(\w+))?)?$": 
                self._process_weather_command
        }

        
    def process(self, speech_input: SpeechInput) -> Command:
        text = speech_input.text.lower()
        
        for pattern, handler in self._command_patterns.items():
            match = re.search(pattern, text)
            if match:
                try:
                    intent, parameters = handler(match)
                    return Command(
                        text=text,
                        intent=intent,
                        parameters=parameters
                    )
                except Exception as e:
                    print(f"Error procesando comando: {e}")
                    continue
        
        return Command(text=text, intent="unknown", parameters={})

    def _process_weather_command(self, match) -> Tuple[str, Dict[str, str]]:
        city = match.group(1).strip()
        day = match.group(2)
        month = match.group(3)
        
        if not day:
            forecast_date = date.today()
        else:
            # Simple month mapping
            months = {
                'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
                'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
                'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
            }
            
            today = date.today()
            month_num = months.get(month.lower()) if month else today.month
            year = today.year
            
            try:
                forecast_date = date(year, month_num, int(day))
                if forecast_date < today:
                    if month and month_num <= today.month:
                        forecast_date = date(year + 1, month_num, int(day))
                    else:
                        raise ValueError("La fecha es en el pasado")
            except ValueError as e:
                raise ValueError(f"Fecha inválida: {str(e)}")
        
        return "weather", {"city": city, "date": forecast_date.isoformat()}