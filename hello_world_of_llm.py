import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Configuration
config = {
    "api_key": os.getenv("API_KEY"),
    "api_version": os.getenv("API_VERSION"),
    "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
    "model_name": os.getenv("MODEL_NAME"),
    "default_headers": {"Ocp-Apim-Subscription-Key": os.getenv("API_KEY")},
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": config["api_key"],
}

# Messages
messages = [
    {"role": "system", "content": "You are an AI assistant"},
    {"role": "user", "content": "Hi, how are you?"},
]

# Make the request
response = requests.post(
    config["azure_endpoint"],
    headers=headers,
    json={"model": config["model_name"], "messages": messages},
)

# Handle the response
if response.status_code == 200:
    print(response.json())
    print("--success--")
else:
    print("Error occurred:", response.status_code, response.text)
