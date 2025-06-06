import os
import speech_recognition as sr
import pygame
import subprocess
from gtts import gTTS
from gtts.tts import gTTSError
from io import BytesIO
from typing import Optional
from ...domain.ports.speech_recognition_port import SpeechRecognitionPort
from ...domain.value_objects.speech_input import SpeechInput
from ...domain.value_objects.speech_output import SpeechOutput


class SpeechRecognitionAdapter(SpeechRecognitionPort):
    def __init__(self, device_index: Optional[int] = None):
        self._recognizer = sr.Recognizer()
        self._device_index = device_index
        self._microphone = None
        pygame.mixer.init()
        self._initialize_microphone()

    def _initialize_microphone(self) -> None:
        try:
            self._microphone = sr.Microphone(device_index=self._device_index)
            with self._microphone as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Error initializing microphone: {e}")
            raise RuntimeError(f"Failed to initialize microphone: {str(e)}")

    def listen(self) -> SpeechInput:
        try:
            with self._microphone as source:
                print("\nEscuchando...")
                audio = self._recognizer.listen(source, timeout=3, phrase_time_limit=8)
                
                print("Procesando audio...")
                text = self._recognizer.recognize_google(audio, language="es-ES")
                print(f"Reconocido: {text}")
                return SpeechInput(text=text, confidence=1.0)
                
        except sr.WaitTimeoutError:
            print("Timeout - No se detectó audio")
            return SpeechInput(text="", confidence=0.0)
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return SpeechInput(text="", confidence=0.0)
        except sr.RequestError as e:
            print(f"Error en el servicio de Google: {e}")
            return SpeechInput(text="", confidence=0.0)
        except Exception as e:
            print(f"Error inesperado: {e}")
            return SpeechInput(text="", confidence=0.0)

    def speak(self, output: SpeechOutput) -> None:
        """
        Convert text to speech and play it using gTTS and pygame.
        
        Args:
            output (SpeechOutput): Object containing text to be spoken
            
        Raises:
            gTTSError: If there's an error generating speech from text
            pygame.error: If there's an error playing the audio
            IOError: If there's an error handling the audio file
        """

        gTTS.GOOGLE_TTS_MAX_CHARS = 1000 
        
        try:
            # Generate speech
            tts = gTTS(text=output.text, lang='es', tld='es', slow=False, lang_check=False)


            with BytesIO() as audio_file:
                tts.write_to_fp(audio_file)
                audio_file.seek(0)

                res = subprocess.run(
                    ['ffmpeg', '-i', 'pipe:0', '-filter:a', 'atempo=1.3', '-f', 'wav', 'pipe:1'],
                    shell=True,
                    input=audio_file.read(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                ).stdout


                audio_file = BytesIO(res)

                                # Load and play audio
                try:
                    pygame.mixer.music.load(audio_file)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to finish
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                        
                except pygame.error as e:
                    print(f"Error playing audio: {str(e)}")
                finally:
                    try:
                        pygame.mixer.music.unload()
                    except pygame.error as e:
                        print(f"Error unloading audio: {str(e)}")
                        
        except gTTSError as e:
            print(f"Error generating speech: {str(e)}")
        except IOError as e:
            print(f"Error handling audio file: {str(e)}")


        #     try:
        #         # Generate MP3
        #         tts.save(temp_mp3)
                
        #         # Convert to WAV with speed adjustment
        #         ffmpeg_cmd = [
        #             'ffmpeg',
        #             '-i', temp_mp3,
        #             '-filter:a', 'atempo=1.3', 
        #             '-y',  # Overwrite output file
        #             temp_wav
        #         ]
                
        #         subprocess.run(
        #             ffmpeg_cmd,
        #             check=True,
        #             capture_output=True
        #         )
                
        #         # Play the processed audio
        #         pygame.mixer.music.load(temp_wav)
        #         pygame.mixer.music.play()
                
        #         # Wait for playback to finish
        #         while pygame.mixer.music.get_busy():
        #             pygame.time.wait(100)
                    
        #     finally:
        #         # Clean up temporary files
        #         for temp_file in [temp_mp3, temp_wav]:
        #             try:
        #                 if os.path.exists(temp_file):
        #                     os.remove(temp_file)
        #             except Exception as e:
        #                 print(f"Error cleaning up {temp_file}: {e}")
        # except Exception as e:
        #     print(f"Error during speech synthesis: {e}")
        # finally:
        #     try:
        #         pygame.mixer.music.unload()
        #     except Exception as e:
        #         print(f"Error unloading music from pygame mixer: {e}")


