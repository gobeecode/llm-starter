from llms.ollama.ollama_client import OllamaClient
import time

class CodingAssistant:
    def __init__(self):
        self.ollama_client = OllamaClient()


    def get_coding_prompt_object(self, code_snippet: str):
        system_prompt = 'You are an expert in coding and can explain the code written in various programming languages.'
        print(f'System prompt: {system_prompt}')
        user_prompt = 'Explain what the below code does and why?'
        user_prompt += f'{code_snippet}'
        print(f'User prompt: {user_prompt}')
        prompt_object = self.ollama_client.get_prompt_object(system_prompt, user_prompt)
        print(f'Prompt object: {prompt_object}')
        return prompt_object

    def explain_code(self, code_snippet: str):
        messages = self.get_coding_prompt_object(code_snippet)
        response = self.ollama_client.ask(messages=messages, stream=True)
        for chunk in response:
            # Each chunk is a dict like: {'message': {'content': '...'}, ...}
            print(chunk['message']['content'], end='', flush=True)

if __name__ == '__main__':
    code_snippet = '''
    yield from {(book.get("year") for book in books if book.get("year"))}
    '''
    coding_assistant = CodingAssistant()
    coding_assistant.explain_code(code_snippet)
