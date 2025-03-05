import speech_recognition as sr
import pyttsx3
from config import VOICE_CONFIG
import warnings
warnings.filterwarnings('ignore')

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.use_voice_input = False
        self.use_voice_output = False

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
            self.use_voice_output = True
            print("Voice output initialized successfully")

        except Exception as e:
            print(f"Voice output initialization error: {e}")
            print("Running in text-only output mode")
            self.engine = None

        try:
            # Check if any microphones are available
            mics = sr.Microphone.list_microphone_names()
            if not mics:
                print("No microphones detected")
                raise Exception("No input devices available")

            # Test microphone access
            with sr.Microphone() as source:
                pass
            self.use_voice_input = True
            print("Voice input initialized successfully")

        except Exception as e:
            print(f"Voice input initialization error: {e}")
            print("Running in text-only input mode")
            print("Note: To use voice commands, please run the assistant on a machine with a working microphone")

    def speak(self, text):
        print("Assistant:", text)  # Always print the response
        if self.use_voice_output and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Speech output error: {e}")
                self.use_voice_output = False  # Disable voice output on error

    def listen(self):
        if self.use_voice_input:
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
                self.speak("I encountered an error while listening. Switching to text input.")
                self.use_voice_input = False  # Disable voice input on error
                return self.listen()  # Retry with text input
        else:
            # Text input mode
            try:
                return input("Enter your command: ").lower().strip()
            except Exception as e:
                print(f"Text input error: {e}")
                return None