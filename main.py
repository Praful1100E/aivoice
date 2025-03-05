import os
import sys
from PyQt5.QtWidgets import QApplication
from gui import JarvisUI
from voice_module import VoiceAssistant
from ai_module import AIAssistant
from system_controls import SystemController
from web_services import WebServices

print("Initializing Jarvis Assistant...")

class JarvisAssistant:
    def __init__(self):
        try:
            self.voice = VoiceAssistant()
            self.ai = AIAssistant()
            self.system = SystemController()
            self.web = WebServices()
            print("All components initialized successfully")
        except Exception as e:
            print(f"Initialization error: {e}")
            raise

    def process_command(self, command):
        if not command:
            return "Waiting for command..."

        try:
            print(f"\nProcessing command: {command}")
            response = None

            # Website commands
            if "open youtube" in command:
                response = self.web.open_website("youtube")
            elif "open google" in command:
                response = self.web.open_website("google")

            # Wikipedia queries
            elif "who is" in command or "what is" in command:
                query = command.replace("who is", "").replace("what is", "").strip()
                response = self.web.search_wikipedia(query)

            # System controls
            elif "increase volume" in command:
                self.system.set_volume(80)
                response = "Volume increased"
            elif "decrease volume" in command:
                self.system.set_volume(30)
                response = "Volume decreased"
            elif "increase brightness" in command:
                self.system.set_brightness(80)
                response = "Brightness increased"
            elif "decrease brightness" in command:
                self.system.set_brightness(30)
                response = "Brightness decreased"

            # AI response for other queries
            else:
                print("Generating AI response...")
                response = self.ai.generate_response(command)

            print(f"Response: {response}")
            return response

        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            print(error_msg)
            return error_msg

def main():
    print("Starting Jarvis GUI Application...")
    app = None
    try:
        app = QApplication(sys.argv)
        print("Qt Application initialized successfully")

        jarvis = JarvisAssistant()
        print("Jarvis Assistant initialized")

        def start_listening():
            try:
                window.update_status("Listening...")
                command = jarvis.voice.listen()
                if command:
                    window.update_status(f"Processing: {command}")
                    response = jarvis.process_command(command)
                    if response:
                        window.update_status(f"Response: {response}")
                        jarvis.voice.speak(response)
            except Exception as e:
                error_msg = f"Error processing voice command: {str(e)}"
                print(error_msg)
                window.update_status(error_msg)

        window = JarvisUI(start_listening)
        print("GUI window created")
        window.show()
        print("GUI window shown")

        sys.exit(app.exec_())
    except Exception as e:
        print(f"Critical error initializing application: {e}")
        if app is None:
            print("Failed to create QApplication instance")
        sys.exit(1)

if __name__ == "__main__":
    main()