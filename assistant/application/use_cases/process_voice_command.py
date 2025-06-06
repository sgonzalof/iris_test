from dataclasses import dataclass

from browser.application.use_cases.google import GoogleSearchRequest, GoogleSearchUseCase
#from browser.application.use_cases.amazon_music import AmazonMusicSearchRequest
from browser.application.use_cases.youtube import YouTubeSearchRequest, YouTubeSearchUseCase
from browser.infrastructure.adapters.browser_adapter import BrowserAdapter
from ...domain.ports.speech_recognition_port import SpeechRecognitionPort
from ...domain.ports.command_processor_port import CommandProcessorPort
from ...domain.value_objects.speech_output import SpeechOutput
from ...domain.value_objects.comand import Command
from ...application.use_cases.time import GetTimeUseCase
from weather.application.use_cases.get_weather import GetWeatherUseCase, GetWeatherRequest
from weather.infrastructure.adapters.open_weather_adapter import OpenWeatherAdapter
from config import Config

@dataclass
class ProcessVoiceCommandResponse:
    success: bool
    message: str


class ProcessVoiceCommandUseCase:
    def __init__(
        self,
        speech_recognition: SpeechRecognitionPort,
        command_processor: CommandProcessorPort,
        config: Config
    ):
        self._speech = speech_recognition
        self._processor = command_processor
        self._get_time = GetTimeUseCase()
        self._weather_service = GetWeatherUseCase(
            OpenWeatherAdapter(config)
        )
        self._browser = BrowserAdapter()
        self._youtube_search = YouTubeSearchUseCase(self._browser)
        self._google_search = GoogleSearchUseCase(self._browser)    

    def execute(self) -> ProcessVoiceCommandResponse:
        try:
        # 1. Escuchar entrada de voz
            speech_input = self._speech.listen()
            if not speech_input.is_valid():
                return ProcessVoiceCommandResponse(
                    False, "No se detectó ningún comando"
                )

        # 2. Procesar el comando
            command = self._processor.process(speech_input)
            if not command.is_valid:
                return ProcessVoiceCommandResponse(
                    False, 
                    f"No se reconoció ningún comando en: {speech_input.text}"
                )

            # 3. Ejecutar acción según el intent
            response = self._execute_command(command)

            # 4. Responder por voz
            self._speech.speak(SpeechOutput(text=response))

            return ProcessVoiceCommandResponse(True, response)

        except Exception as e:
            return ProcessVoiceCommandResponse(False, f"Error: {str(e)}")

    def _execute_command(self, command: Command) -> str:
        try:
            match command.intent:
                case "weather":
                    from datetime import date
                    forecast_date = date.fromisoformat(
                        command.parameters.get('date', date.today().isoformat())
                    )
                    request = GetWeatherRequest(
                        city=command.parameters.get('city'),
                        forecast_date=forecast_date
                    )
                    return self._weather_service.execute(request)
                case "time":
                    response = self._get_time.execute()
                    return response.format_time()
                case "google_search":
                    request = GoogleSearchRequest(
                        query=command.parameters["query"],
                        description="Búsqueda en Google"
                    )
                    return self._google_search.execute(request)

                case "youtube_search":
                    request = YouTubeSearchRequest(query=command.parameters["query"])
                    return self._youtube_search.execute(request)
                # case "amazon_music_search":
                #     request = AmazonMusicSearchRequest(query=command.parameters["query"])
                #     return self._amazon_music_search.execute(request)
                case _:
                    return print(f"Comando no reconocido: {command.intent}")
        except Exception as e:
            return f"Error procesando el comando: {str(e)}"