import sys
from PyQt5.QtWidgets import QApplication
from gui import JarvisUI
from voice_module import VoiceAssistant
from ai_module import AIAssistant
from system_controls import SystemController
from web_services import WebServices

class JarvisAssistant:
    def __init__(self):
        self.voice = VoiceAssistant()
        self.ai = AIAssistant()
        self.system = SystemController()
        self.web = WebServices()
        
    def process_command(self, command):
        if not command:
            return
            
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
            
        # Weather information
        elif "weather in" in command:
            city = command.split("weather in")[-1].strip()
            response = self.web.get_weather(city)
            
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
            response = self.ai.generate_response(command)
        
        if response:
            self.voice.speak(response)
            return response

def main():
    app = QApplication(sys.argv)
    
    jarvis = JarvisAssistant()
    
    def start_listening():
        command = jarvis.voice.listen()
        if command:
            window.update_status(f"Processing: {command}")
            response = jarvis.process_command(command)
            window.update_status(f"Response: {response}")
    
    window = JarvisUI(start_listening)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
