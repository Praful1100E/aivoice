import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import MODEL_CONFIG
import warnings
warnings.filterwarnings('ignore')

class AIAssistant:
    def __init__(self):
        self.model_name = MODEL_CONFIG["model_name"]
        self.model = None
        self.tokenizer = None
        self.initialize_model()

    def initialize_model(self):
        try:
            print("Loading AI model...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                **MODEL_CONFIG["tokenizer_kwargs"]
            )
            
            # Set padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **MODEL_CONFIG["model_kwargs"]
            )
            
            # Configure model settings
            self.model.config.pad_token_id = self.tokenizer.pad_token_id
            self.model.config.eos_token_id = self.tokenizer.eos_token_id
            
            # Move to GPU if available
            if torch.cuda.is_available():
                self.model = self.model.cuda()
            
            print("AI model loaded successfully!")
        except Exception as e:
            print(f"Error loading AI model: {e}")
            raise

    def generate_response(self, prompt):
        try:
            messages = [{"role": "user", "content": str(prompt).strip()}]
            input_text = self.tokenizer.apply_chat_template(messages, tokenize=False)
            
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=256,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1,
                    no_repeat_ngram_size=3
                )
            
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            answer = answer.replace(input_text, "").strip()
            
            return answer if answer else "I apologize, but I couldn't generate a proper response."
        except Exception as e:
            return f"AI Error: {str(e)}"
