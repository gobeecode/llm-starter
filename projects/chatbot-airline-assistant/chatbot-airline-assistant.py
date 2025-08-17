from llms.ollama.ollama_client import OllamaClient
import gradio as gr
import json

ollama_client = OllamaClient()
system_message = "You are a helpful assistant for an airline called FlightAI. "
system_message += "Give short courteous answers no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer then say so."


def get_ticket_price(destination_city: str):
    ticket_prices = {"switzerland": "$999", "paris": "$1899", "dubai": "$799", "london": "$799", "italy": "$599"}
    print(f"Tool call ticket prices for '{destination_city}'.")
    city = destination_city.lower()
    return ticket_prices.get(city, "unknown")


def handle_tool_call(tool_data):
    city = tool_data.get("destination_city")
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price})
    }
    return response, city

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of the ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city where the customer wants to travel to.",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
tools = [{"type": "function", "function": price_function}]

def chat(message, history):
    messages = [{"role": "system", "content": system_message}]
    for user_message, assistant_message in history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": assistant_message})
    messages.append({"role": "user", "content": message})
    response = ollama_client.ask(messages=messages, tools=tools)
    tool_call = response["message"]["tool_calls"][0]
    tool_name = tool_call["function"]["name"]
    tool_args = tool_call["function"]["arguments"]
    print(f"Tool requested: {tool_name} with args {tool_args}")
    message = response["message"]
    response, city = handle_tool_call(tool_args)
    messages.append(message)
    messages.append(response)
    response = ollama_client.ask(messages=messages, stream=True)
    result = ""
    for chunk in response:
        result += chunk['message']['content']
        yield result

if __name__ == '__main__':
    view = gr.ChatInterface(fn=chat)
    view.launch(share=False)