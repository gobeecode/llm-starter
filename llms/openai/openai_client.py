import json

from openai import OpenAI, NotGiven
from openai.types import ResponseFormatText

from config.environment import get_environment_key_value
from utils.timer import Timer

from typing import Optional, List, Dict, Any
import openai

from config.environment import get_environment_key_value
from llms.base.llm_client import LLMClient
from utils.timer import Timer


class OpenAIClient(LLMClient):
    """
    Reusable client for interacting with OpenAI models.
    """

    def __init__(self, timer_enabled = False):
        super().__init__()
        self.timer_enabled = timer_enabled
        self._response = None
        self._openai = OpenAI()

    def validate_openai_api_key(self):
        key_name = 'OPENAI_API_KEY'
        api_key = get_environment_key_value(key_name)
        if not api_key.startswith("sk-"):
            raise ValueError(f"{key_name} must start with 'sk-'.")

    def ask(self, messages: List, model: Optional[str] = None, stream: bool = False,
            response_format: ResponseFormatText | NotGiven = None):
        """
        Sends a message list to the OpenAI model and returns the full response.
        """
        model_to_use = model or get_environment_key_value('MODEL')
        print(f"Model: {model_to_use}")
        print("Waiting for OpenAI's response... Please wait.")
        #
        # if self.timer_enabled:
        #     Timer.start("openai")
        self._response = self._openai.chat.completions.create(
            model=model, messages=messages, response_format=response_format)
        # if self.timer_enabled:
        #     Timer.stop("openai")
        #     elapsed = Timer.elapsed("openai")
        #     print(f"OpenAI's response took {elapsed:.2f} seconds.")

        return self._response


