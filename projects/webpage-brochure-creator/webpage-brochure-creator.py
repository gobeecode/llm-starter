from llms.ollama.ollama_client import OllamaClient
from models.website import Website
from utils.parser import parse_string_as_json

from utils.path_handler import get_output_directory
from utils.file_handler import write_contents_to_file
from utils.timer import Timer

class WebpageBrochureCreator:


    def __init__(self, url: str):
        self.website = Website(url)
        self.ollama_client = OllamaClient()

    def get_links_prompt_object(self):
        links = self.website.get_links()
        system_prompt = ('You are provided with a list of links found in a website.'
                         'You are able to decide which links are relevant to be included in the company brochure '
                         'such as the about page, contact page, careers page, etc. '
                         'Ensure that the response is only a json object without any additional information.'
                         'The response should exactly match the format below. '
                         'The response should start with opening curly brace and end with closing curly brace.')
        system_prompt += '''
          {  
              "links": [
                  {"type": "about", "url": "https://example.com/about"},
                  {"type": "contact", "url": "https://example.com/contact"}
                ]
          }
          '''
        print(f'System prompt: {system_prompt}')
        user_prompt = ("Respond with full https URLs. Do not include privacy policy or terms of service links. "
                       "Do not include entries that has empty or invalid links. "
                       "Please provide a JSON response with relevant links"
                       "Validate the json response and remove any invalid characters found in the response. "
                       "Here are the links found in the website")
        user_prompt += "\n".join(links)
        print(f'User prompt: {user_prompt}')
        prompt_object = self.ollama_client.get_prompt_object(system_prompt, user_prompt)
        print(f'Prompt object: {prompt_object}')
        return prompt_object


    def get_all_links(self):
        prompt_object = self.get_links_prompt_object()
        # response = ask_openai(prompt_object)
        print('Getting all links...')
        response = self.ollama_client.ask(messages=prompt_object, stream=True)
        response_content = ""
        for chunk in response:
            content = chunk.get("message", {}).get("content", "")
            print(content, end='', flush=True)
            response_content += content

        print(response_content)
        json_response = parse_string_as_json(response_content)
        links = json_response.get('links')
        return links

    def get_all_webpage_details(self):
        links = self.get_all_links()
        print('Getting all webpage details...')
        self.result = ''
        for link in links:
            try:
                link_type = link.get('type')
                link_url = link.get('url')
                print(f'Fetching webpage details of {link_type} with url: {link_url}...')
                contents = Website(link_url).get_content()
                self.result += f'\n\n{link_type}'
                self.result += f'\n{contents}'
            except Exception as e:
                print(f'Failed to fetch webpage details of {link_type}: {e}')
        return self.result


    def get_create_brochure_prompt_object(self, company_name: str):
        system_prompt = ('You are an assistant that analyzes the contents of several relevant pages of a company '
                         'website and creates a short brochure about the company for prospective customers, investors '
                         'and recruits. Include details of the company culture, customers, careers if you have that '
                         'information. You should respond in markdown format.')
        print(f'System prompt: {system_prompt}')
        user_prompt = (f'You are looking at a company called {company_name}. Here are the contents of the landing page '
                       f'and relevant pages. Use this information to build a short brochure about the company.')
        user_prompt += f'{self.get_all_webpage_details()}'
        print(f'User prompt: {user_prompt}')
        prompt_object = self.ollama_client.get_prompt_object(system_prompt, user_prompt)
        print(f'Prompt object: {prompt_object}')
        return prompt_object

    def create_brochure(self, company_name: str):
        Timer.start("Create Brochure")
        prompt_object = self.get_create_brochure_prompt_object(company_name)
        print('Creating brochure...')
        response = self.ollama_client.ask(messages=prompt_object, stream=True)
        response_content = ""
        for chunk in response:
            content = chunk.get("message", {}).get("content", "")
            print(content, end='', flush=True)
            response_content += content
        print(response_content)
        output_directory = get_output_directory()
        formatted_company_name = '_'.join(company_name.lower().split(' '))
        formatted_file_name = f'{output_directory}/brochure_{formatted_company_name}.md'
        write_contents_to_file(formatted_file_name, response_content)
        Timer.stop("Create Brochure")
        elapsed = Timer.elapsed("Create Brochure")
        print(f'Brochure created in {elapsed} seconds.')

if __name__ == '__main__':
    webpage_brochure_creator = WebpageBrochureCreator(url='https://anthropic.com')
    webpage_brochure_creator.create_brochure('Anthropic')



