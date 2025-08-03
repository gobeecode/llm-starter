from http.client import responses

from llms.base import get_messages
from llms.ollama import ask_ollama
from llms.openai import ask_openai
from models.website import Website


class WebpageSummarizer:
    def __init__(self, url: str):
        self.website = Website(url)

    def get_summarize_messages(self):
        title = self.website.get_title()
        contents = self.website.get_content()
        system_prompt = '''You are an AI assistant that summarizes webpages. 
                Provide a concise summary of the content. 
                Ignore any HTML tags and navigation related text and focus on the main text. 
                Respond in markdown format.'''
        print(f'System prompt: {system_prompt}')
        user_prompt = f'''Summarize the content of the webpage {url} with the title "{title}". 
                The content of the website is as follows:\n{contents}'''
        print(f'User prompt: {user_prompt}')
        messages = get_messages(system_prompt, user_prompt)
        print(f'Messages: {messages}')
        return messages

    def summarize_webpage_using_openai(self):
        messages = self.get_summarize_messages()
        response = ask_openai(model, messages)
        print(response)

    def summarize_webpage_using_ollama(self):
        messages = self.get_summarize_messages()
        response = ask_ollama(model, messages)
        print(response)

if __name__ == '__main__':
    webpage_summarizer = WebpageSummarizer(url='https://wikipedia.org/')
    # webpage_summarizer.summarize_webpage_using_openai(url)
    webpage_summarizer.summarize_webpage_using_ollama()
