
def get_messages(system_prompt: str, user_prompt: str):
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    return messages