import sys
from voice_module import VoiceAssistant
from ai_module import AIAssistant
from system_controls import SystemController
from web_services import WebServices

class JarvisAssistantCLI:
    def __init__(self):
        print("Initializing Jarvis Assistant...")
        try:
            self.voice = VoiceAssistant()
            self.ai = AIAssistant()
            self.system = SystemController()
            self.web = WebServices()
            print("\nJarvis is ready! Speak a command or say 'exit' to quit.")
        except Exception as e:
            print(f"Critical initialization error: {e}")
            sys.exit(1)

    def process_command(self, command):
        if not command:
            return None

        # Handle exit command
        if command.lower() in ['exit', 'quit', 'stop']:
            print("\nGoodbye!")
            sys.exit(0)

        print(f"\nProcessing command: {command}")
        response = None

        try:
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

            if response:
                print(f"\nResponse: {response}")
                self.voice.speak(response)
            return response

        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            print(error_msg)
            self.voice.speak("Sorry, I encountered an error processing your command.")
            return error_msg

def main():
    try:
        print("\nStarting Jarvis Voice Assistant...")
        print("Initializing components...")

        jarvis = JarvisAssistantCLI()

        while True:
            print("\nListening for your command...")
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