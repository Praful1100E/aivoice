import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import MODEL_CONFIG
import warnings
import time
warnings.filterwarnings('ignore')

class AIAssistant:
    def __init__(self):
        self.model_name = MODEL_CONFIG["model_name"]
        self.model = None
        self.tokenizer = None
        self.max_retries = 3
        print(f"AI Assistant initialized, using model: {self.model_name}")

    def initialize_model(self):
        if self.model is not None:
            return True

        retries = 0
        while retries < self.max_retries:
            try:
                # Set environment variables for optimization
                os.environ["TRANSFORMERS_CACHE"] = "./model_cache"
                os.environ["HF_HOME"] = "./model_cache"

                print("\nLoading AI model components...")
                print("Step 1/4: Loading tokenizer...")
                # Load tokenizer
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    **MODEL_CONFIG["tokenizer_kwargs"]
                )
                print("Tokenizer loaded successfully")

                # Set padding token
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                    self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
                    print("Padding token configured")

                print("Step 2/4: Loading base model (this may take a few moments)...")
                # Load model
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    **MODEL_CONFIG["model_kwargs"]
                )
                print("Base model loaded successfully")

                print("Step 3/4: Configuring model settings...")
                # Configure model settings
                self.model.config.pad_token_id = self.tokenizer.pad_token_id
                self.model.config.eos_token_id = self.tokenizer.eos_token_id

                print("Step 4/4: Optimizing model placement...")
                # Move to GPU if available
                if torch.cuda.is_available():
                    print("Moving model to GPU...")
                    self.model = self.model.cuda()
                    print("Model moved to GPU successfully")
                else:
                    print("Running on CPU (GPU not available)")

                print("AI model initialization complete!")
                return True

            except Exception as e:
                retries += 1
                print(f"\nError during model initialization (attempt {retries}/{self.max_retries}): {e}")
                if retries < self.max_retries:
                    print(f"Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    print("Failed to initialize AI model after maximum retries")
                    return False

    def generate_response(self, prompt):
        # Lazy loading of the model
        if not self.model and not self.initialize_model():
            return "I apologize, but I'm having trouble initializing. Please try again in a moment."

        try:
            print("\nProcessing your query...")
            # Format input using Qwen's chat template
            messages = [{"role": "user", "content": str(prompt).strip()}]
            input_text = self.tokenizer.apply_chat_template(messages, tokenize=False)
            print("Query formatted for AI model")

            # Tokenize input
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            print("Input tokenized")

            # Move inputs to correct device
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

            # Generate response with optimized parameters
            print("Generating AI response...")
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

            # Process and clean response
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            answer = answer.replace(input_text, "").strip()
            print("Response generated successfully")

            return answer if answer else "I apologize, but I couldn't generate a proper response."
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"