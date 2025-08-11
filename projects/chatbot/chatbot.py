from llms.ollama.ollama_client import OllamaClient
import gradio as gr

class Chatbot:
    def __init__(self):
        self.ollama_client = OllamaClient()
        self.system_message = "You are a helpful assistant."
        self.system_message += "If the customer asks for shoes, you should respond that it is not on sale and suggest them to look at hats instead."

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_message}]
        if "belt" in message:
            messages.append({"role": "system", "content": "For added context, the store does not sell belts, but make sure you point out other items on sale such as balls and books."})
        for user_message, assistant_message in history:
            messages.append({"role": "user", "content": user_message})
            messages.append({"role": "assistant", "content": assistant_message})
        messages.append({"role": "user", "content": message})
        # print(history)
        # print(messages)
        response = self.ollama_client.ask(messages=messages, stream=True)
        result = ""
        for chunk in response:
            result += chunk['message']['content']
            yield result

if __name__ == '__main__':
    chatbot = Chatbot()
    view = gr.ChatInterface(
        fn=chatbot.chat,
    )
    view.launch(share=False)