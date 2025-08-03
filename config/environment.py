import os
from dotenv import load_dotenv

load_dotenv()

def get_environment_key_value(key: str):
    value = os.getenv(key)
    if not value:
        raise ValueError(f"'{key}' environment variable not set.")