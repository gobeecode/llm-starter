from llms.ollama.ollama_client import OllamaClient
import time

class Joker:
    def __init__(self):
        self.ollama_client = OllamaClient()


    def get_joke_prompt_object(self, topic: str):
        system_prompt = 'You are an expert in jokes and will be able to instantly crack jokes on any topic.'
        print(f'System prompt: {system_prompt}')
        user_prompt = f'Tell me a random and unique joke on {topic}'
        print(f'User prompt: {user_prompt}')
        prompt_object = self.ollama_client.get_prompt_object(system_prompt, user_prompt)
        print(f'Prompt object: {prompt_object}')
        return prompt_object

    def tell_a_joke(self, topic: str):
        messages = self.get_joke_prompt_object(topic)
        response = self.ollama_client.ask(messages=messages, stream=True)
        for chunk in response:
            # Each chunk is a dict like: {'message': {'content': '...'}, ...}
            print(chunk['message']['content'], end='', flush=True)

if __name__ == '__main__':
    topic = 'Data scientist'
    joker = Joker()
    joker.tell_a_joke(topic)
