import os

# API Keys and Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")

# AI Model Configuration
MODEL_CONFIG = {
    "model_name": "Qwen/Qwen2.5-0.5B",  # Updated to Qwen 2.5 free version
    "model_kwargs": {
        "trust_remote_code": True,
        "device_map": "auto",
        "low_cpu_mem_usage": True,
        "torch_dtype": "float16",
        "use_flash_attention_2": False,
        "use_cache": True
    },
    "tokenizer_kwargs": {
        "trust_remote_code": True,
        "padding_side": 'left'
    }
}

# Voice Configuration
VOICE_CONFIG = {
    "language": "en-US",
    "sample_rate": 16000
}