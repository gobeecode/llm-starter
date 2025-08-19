from llms.ollama.ollama_client import OllamaClient
from models.website import Website


class WebpageSummarizer:
    def __init__(self, url: str):

        self.website = Website(url)
        self.ollama_client = OllamaClient()

    def get_summarize_prompt_object(self):
        title = self.website.get_title()
        contents = self.website.get_content()
        system_prompt = '''You are an AI assistant that summarizes webpages. 
                Provide a concise summary of the content. 
                Ignore any HTML tags and navigation related text and focus on the main text. 
                Respond in markdown format.'''
        print(f'System prompt: {system_prompt}')
        user_prompt = f'''Summarize the content of the webpage {self.website.url} with the title "{self.website.get_title()}". 
                The content of the website is as follows:\n{self.website.get_content()}'''
        print(f'User prompt: {user_prompt}')
        prompt_object = self.ollama_client.get_prompt_object(system_prompt, user_prompt)
        print(f'Prompt object: {prompt_object}')
        return prompt_object

    def summarize_webpage(self):
        messages = self.get_summarize_prompt_object()
        # For openAI call this line.
        # response = ask_openai(model, messages)
        response = self.ollama_client.ask(messages)
        response_content = response['message']['content']
        print(response_content)

if __name__ == '__main__':
    webpage_summarizer = WebpageSummarizer(url='https://wikipedia.org/')
    webpage_summarizer.summarize_webpage()
