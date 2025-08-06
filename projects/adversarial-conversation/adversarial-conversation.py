from llms.ollama.ollama_client import OllamaClient

ollama_client = OllamaClient()

model1 = 'llama3.2:1b'
model1_name = 'Ramesh'
model1_mood = 'romantic'

model2 = 'gemma3:4b'
model2_name = 'Priya'
model2_mood = 'rude'

def call_model1():
    model1_system_message = f'You are a chatbot who is very {model1_mood}.'
    messages = [{"role": "system", "content": model1_system_message}]
    for model1_message, model2_message in zip(model1_messages, model2_messages):
        messages.append({"role": "assistant", "content": model1_message})
        messages.append({"role": "user", "content": model2_message})
    response = ollama_client.ask(model=model1, messages=messages, stream=False)
    return str(response['message']['content']).replace('\n', '')


def call_model2():
    model2_system_message = f'You are a chatbot who is very {model2_mood}.'
    messages = [{"role": "system", "content": model2_system_message}]
    for model1_message, model2_message in zip(model1_messages, model2_messages):
        messages.append({"role": "user", "content": model1_message})
        messages.append({"role": "assistant", "content": model2_message})
    messages.append({"role": "user", "content": model1_messages[-1]})
    response = ollama_client.ask(model=model2, messages=messages, stream=False)
    return str(response['message']['content']).replace('\n\n', '')


if __name__ == '__main__':
    model1_messages = ['Hi there!']
    model2_messages = ['Hi!']
    print(f'{model1_name}: {model1_messages[0]}')
    print(f'{model2_name}: {model2_messages[0]}')
    for i in range(5):
        model1_next = call_model1()
        print(f"{model1_name}: {model1_next}")
        model1_messages.append(model1_next)
        model2_next = call_model2()
        print(f"{model2_name}: {model2_next}")
        model2_messages.append(model2_next)
