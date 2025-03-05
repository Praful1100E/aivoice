# Jarvis AI Voice Assistant 🤖🎙️

Jarvis is an AI-powered voice assistant designed to make your digital experience smarter and more efficient. It combines powerful speech recognition, AI chatbot capabilities, and web automation, making it easy to interact with your computer using just your voice. With features like weather updates, system controls, and Wikipedia search, Jarvis is your go-to assistant for everyday tasks!

---

## Features ✨

- **Speech Recognition**: Listens to voice commands and processes them accurately.
- **AI Chatbot**: Uses the Qwen 2.5-0.5B model to generate intelligent, context-aware responses.
- **Text-to-Speech**: Converts text-based responses into natural-sounding speech.
- **Web Automation**: Opens websites like YouTube, Google, and more with voice commands.
- **Wikipedia Search**: Fetches concise summaries from Wikipedia for quick information retrieval.
- **Weather Updates**: Provides real-time weather data for any location globally 🌦️.
- **System Controls**: Adjusts system volume and screen brightness with voice commands 🔊💡.
- **User Interface**: Simple GUI powered by PyQt5 for easy interaction and setup.

---

## Installation 🛠️

### Prerequisites

- Python 3.8+ is required. 
- Install dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### Required Dependencies

Ensure the following libraries are installed:

```bash
pip install speechrecognition pyttsx3 webbrowser wikipedia requests pyautogui screen-brightness-control pycaw torch transformers PyQt5
```

---

## Usage 🚀

### 1. Run the Assistant

Once installed, you can start the assistant by running the command:

```bash
python jarvis.py
```

### 2. Use the GUI

- Click the **"Speak"** button in the graphical user interface (GUI).
- Say your command aloud.
- Jarvis will process the command and respond accordingly.

---

## Example Commands 🗣️

- **"What's the weather like in New York?"** 🌆
- **"Open YouTube"** 🎥
- **"Turn the volume up"** 🔊
- **"Search for artificial intelligence on Wikipedia"** 📚
- **"What time is it?"** ⏰

---

## Configuration ⚙️

To enable weather updates, you’ll need an API key from [OpenWeatherMap](https://openweathermap.org/). Once you have your key:

1. Replace `"YOUR_OPENWEATHERMAP_API_KEY"` in the `get_weather()` function inside the `jarvis.py` file.
2. Save the changes and restart the assistant.

---

## Future Enhancements 🔮

- Add support for more advanced AI models.
- Improve natural language understanding for more intuitive interactions.
- Expand system automation to support additional tasks like file management and email handling.
- Voice-based control for third-party applications like Spotify, Netflix, etc.

---

## Contributing 💡

We welcome contributions! To get started:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request.

Feel free to suggest new features, report bugs, or improve documentation.

---

## License 📜

This project is open-source and licensed under the [MIT License](LICENSE).

---

## Author 👨‍💻

Developed by [Praful Thakur]

---
