import gradio as gr

from llms.ollama.ollama_client import OllamaClient

ollama_client = OllamaClient()

def shout(text: str):
    return text.upper()

def ask_ollama(text: str):
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant who responds in markdown'},
        {'role': 'user', 'content': text},
    ]
    # Without streaming
    # response = ollama_client.ask(messages=messages, stream=False)
    # return response['message']['content']

    # With streaming
    response = ollama_client.ask(messages=messages, stream=True)
    result = ""
    for chunk in response:
        result += chunk['message']['content']
        yield result

if __name__ == '__main__':
    # Basic interface
    # view = gr.Interface(fn=shout, inputs="textbox", outputs="text")
    # view = gr.Interface(
    #         fn=ask_ollama,
    #         inputs=[gr.Textbox(label='Your message', lines=6)],
    #         outputs=[gr.Textbox(label='Response', lines=8)],
    #         allow_flagging='never'
    #     )
    view = gr.Interface(
            fn=ask_ollama,
            inputs=[gr.Textbox(label='Your message', lines=6)],
            outputs=[gr.Markdown(label='Response')],
            allow_flagging='never'
        )
    view.launch(share=False)