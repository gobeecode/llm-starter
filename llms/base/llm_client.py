from typing import List, Dict, Optional, Any


class LLMClient:
    """
    Strategy interface for language model clients.
    """

    def __init__(self):
        self.messages = None

    def get_prompt_object(self, system_prompt: str, user_prompt: str):
        self.messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        return self.messages

    def ask(self, messages: List[Dict[str, str]], model: Optional[str] = None, stream: bool = False) -> Any:
        raise NotImplementedError