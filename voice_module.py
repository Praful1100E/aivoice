import speech_recognition as sr
import pyttsx3
from config import VOICE_CONFIG

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.use_voice = True
        try:
            with sr.Microphone() as source:
                pass
            print("Voice input initialized successfully")
        except Exception as e:
            print(f"Microphone initialization failed: {e}")
            print("Falling back to text input mode")
            self.use_voice = False

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
            # Fallback to printing if speech fails
            print(f"Assistant: {text}")

    def listen(self):
        if self.use_voice:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    self.recognizer.adjust_for_ambient_noise(source)
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
                print(f"Voice input error: {e}")
                print("Switching to text input mode...")
                self.use_voice = False
                return self.listen()
        else:
            # Text input fallback
            try:
                command = input("Enter your command: ").lower()
                return command
            except Exception as e:
                print(f"Text input error: {e}")
                return ""