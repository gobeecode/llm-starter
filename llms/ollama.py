import ollama

model = 'llama3.2'

def ask_ollama(messages):
    print(f'Model: {model}')
    print('Waiting for Ollama\'s response...')
    print('Please wait! This might take a while...')
    response = ollama.chat(model=model, messages=messages)
    return response['message']['content']
