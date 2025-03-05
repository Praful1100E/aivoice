# Jarvis AI Voice Assistant

A Python-based voice assistant with AI integration, system controls, and GUI interface. This project combines voice recognition, text-to-speech, and AI capabilities to create an interactive assistant that can perform various tasks.

## Features

- Voice and text input support
- Text-to-speech output with configurable voice settings
- GUI interface built with PyQt5
- Wikipedia search integration
- Web browser control (YouTube, Google)
- System controls (volume, brightness) - simulated
- AI-powered conversations using Qwen 2.5
- Fallback to text mode when voice hardware is unavailable

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

2. Install the required dependencies:
```bash
pip install PyQt5 pyttsx3 SpeechRecognition PyAudio wikipedia torch transformers screen-brightness-control comtypes pycaw
```

## Usage

The assistant can be run in two modes:

### CLI Mode
```bash
python cli.py
```

### GUI Mode
```bash
python main.py
```

## Voice Commands

- "What is [topic]" - Search Wikipedia
- "Who is [person]" - Search Wikipedia
- "Open youtube" - Opens YouTube in default browser
- "Open google" - Opens Google in default browser
- "Increase volume" - Increases system volume
- "Decrease volume" - Decreases system volume
- "Increase brightness" - Increases screen brightness
- "Decrease brightness" - Decreases screen brightness
- Any other query will be processed by the AI model

## Project Structure

- `main.py` - GUI application entry point
- `cli.py` - Command-line interface entry point
- `gui.py` - PyQt5-based user interface
- `voice_module.py` - Speech recognition and synthesis
- `ai_module.py` - AI model integration
- `web_services.py` - Web-related functionality
- `system_controls.py` - System control operations
- `config.py` - Configuration settings

## Requirements

- Python 3.8+
- Working microphone (optional, falls back to text input)
- Internet connection for AI model and speech recognition
- GPU recommended but not required (falls back to CPU)

## License

MIT License - feel free to use and modify as needed.
