import sys
from voice_module import VoiceAssistant
from ai_module import AIAssistant
from system_controls import SystemController
from web_services import WebServices

class JarvisAssistantCLI:
    def __init__(self):
        print("Initializing Jarvis Assistant...")
        self.voice = VoiceAssistant()
        self.ai = AIAssistant()
        self.system = SystemController()
        self.web = WebServices()

    def process_command(self, command):
        if not command:
            return "Waiting for command..."

        print(f"Processing command: {command}")
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
            response = "Volume increased (Simulated)"
        elif "decrease volume" in command:
            self.system.set_volume(30)
            response = "Volume decreased (Simulated)"
        elif "increase brightness" in command:
            self.system.set_brightness(80)
            response = "Brightness increased"
        elif "decrease brightness" in command:
            self.system.set_brightness(30)
            response = "Brightness decreased"

        # AI response for other queries
        else:
            response = self.ai.generate_response(command)

        if response:
            print(f"Response: {response}")
            self.voice.speak(response)
        return response

def main():
    try:
        print("Starting Jarvis Assistant in CLI mode...")
        jarvis = JarvisAssistantCLI()
        print("Initialization complete. Ready for voice commands.")

        while True:
            command = jarvis.voice.listen()
            if command:
                jarvis.process_command(command)

    except KeyboardInterrupt:
        print("\nExiting Jarvis Assistant...")
        sys.exit(0)
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()