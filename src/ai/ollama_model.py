import requests 
from .ai_model_interface import AIModel

class OllamaModel(AIModel):
    """
    Local LLM implementation using Ollama.
    Requires:
      - Ollama installed on the system
      - A model pulled (e.g., `ollama pull phi3`)
    """

    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to the local Ollama server and return the model's response.
        """
        response = requests.post(
            self.url,
            json = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        # Basic safety: handle missing or malformed responses
        data = response.json()
        return data.get("response", "")