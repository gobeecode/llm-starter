from llms.base import get_messages
from llms.ollama import ask_ollama
from llms.openai import ask_openai
from models.website import Website

class WebpageBrochureCreator:
    def __init__(self, url: str):
        self.website = Website(url)

    def get_links_messages(self):
        links = self.website.get_links()
        system_prompt = 'You are provided with a list of links found in a website.\nYou are able to decide which links are relevant to be included in the company brochure such as the about page, contact page, careers page, etc.'
        system_prompt += ' You should respond in JSON format as in the example below.'
        system_prompt += '''
          {  
              "links": [
                  {"type": "about", "url": "https://example.com/about"},
                  {"type": "contact", "url": "https://example.com/contact"},
                  {"type": "careers", "url": "https://example.com/careers"}
          }
          '''
        print(f'System prompt: {system_prompt}')
        user_prompt = "Please provide a JSON response with relevant links. Respond with full https URLs. Do not include privacy policy or terms of service links. Do not include entries that has empty or invalid links. "
        user_prompt += f"Here are the links found in the website"
        user_prompt += "\n".join(links)
        print(f'User prompt: {user_prompt}')
        messages = get_messages(system_prompt, user_prompt)
        print(f'Messages: {messages}')
        return messages

    def get_links_for_brochure_with_openai(self):
        messages = self.get_links_messages()
        response = ask_openai(messages)
        print(response)

    def get_links_for_brochure_with_ollama(self):
        messages = self.get_links_messages()
        response = ask_ollama(messages)
        print(response)

if __name__ == '__main__':
    webpage_brochure_creator = WebpageBrochureCreator(url='https://wikipedia.org/')
    # webpage_brochure_creator.get_links_for_brochure_with_openai()
    webpage_brochure_creator.get_links_for_brochure_with_ollama()
