import requests
import json

# Configuration
config = {
    "api_key": "",  # Hardcoded API key
    "api_version": "2024-02-01",
    "azure_endpoint": "https://hub-apim-devtestcore.azure-api.net/private/openai/deployments/gpt-4-turbo/chat/completions?api-version=2024-02-01",
    "model_name": "gpt-4-turbo",
    "default_headers": {
        "Ocp-Apim-Subscription-Key": ""  # Hardcoded API key
    }
}

# Headers
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': config['api_key']
}

# Messages
messages = [
    {"role": "system", "content": "You are an AI assistant"},
    {"role": "user", "content": "Hi, how are you?"}
]

# Make the request
response = requests.post(
    config['azure_endpoint'],
    headers=headers,
    json={
        'model': config['model_name'],
        'messages': messages
    }
)

# Handle the response
if response.status_code == 200:
    print(response.json())
    print('--success--')
else:
    print("Error occurred:", response.status_code, response.text)
