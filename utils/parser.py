import json

from rich.markdown import Markdown
from rich.console import Console

def parse_string_as_json(user_input: str):
    try:
        print('Parsing user input as JSON...')
        print(f'User input: {user_input}')
        json_response = json.loads(user_input)
        print('Parsing user input as JSON successful.')
        return json_response
    except Exception as e:
        raise ValueError(f'Could not parse user input as JSON. Exception: {e}.')


def parse_string_as_markdown(user_input: str):
    try:
        print('Parsing user input as Markdown...')
        print(f'User input: {user_input}')
        markdown_response = Markdown(user_input)
        print('Parsing user input as Markdown successful.')
        return markdown_response
    except Exception as e:
        raise ValueError(f'Could not parse user input as Markdown. Exception {e}.')