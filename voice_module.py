import speech_recognition as sr
import pyttsx3
from config import VOICE_CONFIG

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(
                    audio,
                    language=VOICE_CONFIG["language"]
                ).lower()
                print("You said:", command)
                return command
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't understand that.")
                return ""
            except sr.RequestError:
                self.speak("Network error.")
                return ""
            except Exception as e:
                print(f"Listening error: {e}")
                return ""
