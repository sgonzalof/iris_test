from abc import ABC, abstractmethod
from ..value_objects.speech_input import SpeechInput
from ..value_objects.comand import Command

class CommandProcessorPort(ABC):
    @abstractmethod
    def process(self, speech_input: SpeechInput) -> Command:
        """Procesa el texto y extrae el comando con su intención y parámetros"""
        pass