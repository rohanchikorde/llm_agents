"""
This script uses the LangChain library to generate a summary and interesting facts about a LinkedIn profile.
It performs the following steps:

1. Loads environment variables from a .env file.
2. Configures API settings and headers for making requests to the Azure OpenAI endpoint.
3. Defines a prompt template for generating the summary and interesting facts.
4. Scrapes LinkedIn profile data using a third-party library.
5. Converts the scraped data to a string format.
6. Constructs messages for the OpenAI API request.
7. Makes a POST request to the Azure OpenAI endpoint with the constructed messages.
8. Handles the response and prints the generated output.

Dependencies:
- langchain
- dotenv
- requests
- json
- third_parties.linkedin (for scraping LinkedIn profile data)
"""
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from third_parties.linkedin import scrape_linkedin_profile
import os
import requests
import json

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

if __name__ == "__main__":
    print('Hello LangChain!')

    summary_template = """
    given the Linkedin information {information} about a person, I want you to create a :
    1. A short summary of the person's profile
    2. two interesting facts about the person with pointers as "-" with title as "Interesting Facts" section. Create a section only if there are facts.
    """

    summary_prompt_template = PromptTemplate(
        input_variables=['information'],
        template=summary_template)

    linkedin_data = scrape_linkedin_profile(
        "https://www.linkedin.com/in/eden-marco")
    print('scraped linkedin data successfully')

    # Ensure linkedin_data is a string
    linkedin_data_str = json.dumps(linkedin_data, indent=2) if isinstance(
        linkedin_data, dict) else str(linkedin_data)

    # Messages
    messages = [
        {"role": "system", "content": "You are an AI assistant"},
        {"role": "user", "content": linkedin_data_str},
    ]

    # Make the request
    response = requests.post(
        config["azure_endpoint"],
        headers=headers,
        json={"model": config["model_name"], "messages": messages},
        timeout=20,
    )

    # Handle the response
    if response.status_code == 200:
        response_json = response.json()
        # Extract the output from the response
        output = response_json['choices'][0]['message']['content']
        print('LLM output:', output)
    else:
        print("Error occurred:", response.status_code, response.text)
