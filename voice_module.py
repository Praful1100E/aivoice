import speech_recognition as sr
import pyttsx3
from config import VOICE_CONFIG
import warnings
warnings.filterwarnings('ignore')

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        try:
            # Initialize text-to-speech engine
            self.engine = pyttsx3.init()

            # Configure voice properties
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to set a female voice if available
                female_voice = next((voice for voice in voices if 'female' in voice.name.lower()), voices[0])
                self.engine.setProperty('voice', female_voice.id)

            # Set speech rate (words per minute)
            self.engine.setProperty('rate', VOICE_CONFIG["speech_rate"])

            print("Voice output initialized successfully")

            # Test microphone
            with sr.Microphone() as source:
                pass
            print("Voice input initialized successfully")

        except Exception as e:
            print(f"Voice initialization error: {e}")
            raise  # We want the voice assistant to have voice capabilities

    def speak(self, text):
        try:
            print("Assistant:", text)  # Also print the response
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
            raise  # We want voice output to work

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=VOICE_CONFIG["ambient_duration"])
                audio = self.recognizer.listen(source, timeout=VOICE_CONFIG["timeout"])

                command = self.recognizer.recognize_google(
                    audio,
                    language=VOICE_CONFIG["language"]
                ).lower()
                print("You said:", command)
                return command

        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            self.speak("I'm having trouble accessing the speech recognition service.")
            return None
        except Exception as e:
            print(f"Listening error: {e}")
            self.speak("I encountered an error while listening. Please try again.")
            return None