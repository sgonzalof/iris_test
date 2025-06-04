from abc import ABC, abstractmethod
from ..value_objects.speech_input import SpeechInput
from ..value_objects.speech_output import SpeechOutput

class SpeechRecognitionPort(ABC):
    @abstractmethod
    def listen(self) -> SpeechInput:
        """Captura audio y lo convierte a texto"""
        pass

    @abstractmethod
    def speak(self, output: SpeechOutput) -> None:
        """Convierte texto a voz y lo reproduce"""
        pass