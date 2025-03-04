# Update imports
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import requests
import pyautogui
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

import warnings
warnings.filterwarnings('ignore')  # Suppress warnings

# Initialize Text-to-Speech first
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Initialize Qwen model and tokenizer with optimized settings
try:
    print("Loading AI model...")
    model_name = "Qwen/Qwen2.5-0.5B"
    
    # Configure model loading
    model_kwargs = {
        "trust_remote_code": True,
        "device_map": "auto",
        "low_cpu_mem_usage": True,
        "torch_dtype": torch.float16,
        "use_flash_attention_2": False,  # Disable SDPA
        "use_cache": True
    }
    
    # Load tokenizer with proper settings
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
        padding_side='left'
    )
    
    # Set padding token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    # Load model with optimized settings
    model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
    
    # Configure model settings
    model.config.pad_token_id = tokenizer.pad_token_id
    model.config.eos_token_id = tokenizer.eos_token_id
    
    # Move to GPU if available
    if torch.cuda.is_available():
        model = model.cuda()
    
    print("AI model loaded successfully!")
except Exception as e:
    print(f"Error loading AI model: {e}")
    sys.exit(1)

# Update ask_ai function with improved error handling
def ask_ai(prompt):
    try:
        # Prepare input with proper formatting
        messages = [{"role": "user", "content": str(prompt).strip()}]
        input_text = tokenizer.apply_chat_template(messages, tokenize=False)
        
        # Tokenize with proper padding
        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        # Move inputs to correct device
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Generate with optimized settings
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.1,
                no_repeat_ngram_size=3
            )
        
        # Process response
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = answer.replace(input_text, "").strip()
        
        if not answer:
            answer = "I apologize, but I couldn't generate a proper response."
        
        speak(answer)
        return answer
    except Exception as e:
        speak("Sorry, I encountered an error.")
        error_msg = f"AI Error: {str(e)}"
        print(error_msg)
        return error_msg

# Then test the connection
try:
    print("Testing AI connection...")
    response = ask_ai("Hello, please respond with a short greeting.")
    print("Test response:", response)
except Exception as e:
    print(f"Test connection error: {e}")

# Voice Recognition Function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

# Open Websites
def open_website(command):
    if "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

# Wikipedia Search
def search_wikipedia(query):
    try:
        results = wikipedia.summary(query.strip(), sentences=2)
        speak(results)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results. Please be more specific.")
        return str(e.options[:3])  # Return first 3 options
    except wikipedia.exceptions.PageError:
        speak("No Wikipedia page found.")
        return "Page not found"
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")
        return str(e)

# Weather API Integration
def get_weather(city):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Get free API key from openweathermap.org
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response.get("main"):
            temperature = response["main"]["temp"]
            speak(f"The temperature in {city} is {temperature} degrees Celsius.")
        else:
            speak("City not found.")
    except requests.RequestException:
        speak("Error fetching weather data.")

# Control System Volume
def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume.iid, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        speak(f"Volume set to {level} percent")
    except Exception as e:
        speak("Error adjusting volume")
        print(f"Volume control error: {e}")

# Control Screen Brightness
def set_brightness(level):
    sbc.set_brightness(level)
    speak(f"Brightness set to {level} percent")

# Process Commands
def process_command(command):
    if "open youtube" in command or "open google" in command:
        open_website(command)
    elif "who is" in command or "what is" in command:
        response = search_wikipedia(command.replace("who is", "").replace("what is", ""))
    elif "weather in" in command:
        city = command.split("weather in")[-1].strip()
        get_weather(city)
    elif "increase volume" in command:
        set_volume(80)
    elif "decrease volume" in command:
        set_volume(30)
    elif "increase brightness" in command:
        set_brightness(80)
    elif "decrease brightness" in command:
        set_brightness(30)
    else:
        response = ask_ai(command)  # Changed from ask_gpt to ask_ai
        print("AI:", response)

# GUI for Jarvis
class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis AI")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel("Press the button and speak", self)
        self.button = QPushButton("Speak", self)
        self.button.clicked.connect(self.start_listening)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def start_listening(self):
        self.label.setText("Listening...")  # Show status update
        QApplication.processEvents()  # Force UI update
        command = listen()
        self.label.setText(f"You said: {command}")  # Show user input
        if command:
            process_command(command)

# Run GUI
app = QApplication(sys.argv)
window = JarvisUI()
window.show()
sys.exit(app.exec_())