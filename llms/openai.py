from openai import OpenAI
from config.environment import get_environment_key_value

openai = OpenAI()
model = 'gpt-4o-mini'


def validate_openai_api_key():
    key_name = 'OPENAI_API_KEY'
    api_key = get_environment_key_value(key_name)
    if not api_key.startswith("sk-"):
        raise ValueError(f"{key_name} must start with 'sk-'.")

def ask_openai(messages):
    validate_openai_api_key()
    print(f'Model: {model}')
    print('Waiting for OpenAI\'s response...')
    print('Please wait! This might take a while...')
    response = openai.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content
