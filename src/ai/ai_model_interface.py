from typing import Protocol

class AIModel(Protocol):
    """
    A simple interface that all AI model implementations must follow.
    This keeps your deterministic --> AI pipeline clean and interchangeable.
    """
    def generate(self, prompt: str) --> str:
        """
        Generate text from a given prompt.
        Concrete implementations (OpenAI, Anthropic, Mock) will override this.
        """
        return f"[MOCK AI OUTPUT] {prompt[:120]}..."
    