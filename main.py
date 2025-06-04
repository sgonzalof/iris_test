from assistant.infrastructure.adapters.speech_recognition_adapter import SpeechRecognitionAdapter
from assistant.infrastructure.adapters.command_processor_adapter import CommandProcessorAdapter
from assistant.application.use_cases.process_voice_command import ProcessVoiceCommandUseCase
from config import Config


def main():
    config = Config()
    # Initialize adapters
    speech_adapter = SpeechRecognitionAdapter(
        device_index=config.DEFAULT_MIC_INDEX
        )
    command_processor = CommandProcessorAdapter()
    
    # Create use case
    process_command = ProcessVoiceCommandUseCase(
        speech_recognition=speech_adapter,
        command_processor=command_processor,
        config=config
    )

    print("Asistente iniciado. Di algo...")
    while True:
        response = process_command.execute()
        if not response.success:
            print(f"Error: {response.message}")


if __name__ == "__main__":
    main()

