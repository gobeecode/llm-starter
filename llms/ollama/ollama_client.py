# ollama_client.py

from typing import Optional, List, Dict, Any
import ollama

from config.environment import get_environment_key_value
from llms.base.llm_client import LLMClient
from utils.timer import Timer


class OllamaClient(LLMClient):
    """
    Reusable client for interacting with Ollama models.
    """

    def __init__(self, timer_enabled = False):
        super().__init__()
        self.timer_enabled = timer_enabled
        self._response = None

    def ask(self, messages: List, model: Optional[str] = None, stream: bool = False):
        """
        Sends a message list to the Ollama model and returns the full response.
        """
        model_to_use = model or get_environment_key_value('MODEL')
        # print(f"\nModel: {model_to_use}")
        # print("Waiting for Ollama's response... Please wait.")
        #
        # if self.timer_enabled:
        #     Timer.start("ollama")
        self._response = ollama.chat(model=model_to_use, messages=messages, stream=stream)
        # if self.timer_enabled:
        #     Timer.stop("ollama")
        #     elapsed = Timer.elapsed("ollama")
        #     print(f"Ollama's response took {elapsed:.2f} seconds.")

        return self._response

