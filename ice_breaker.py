"""
This script uses the LangChain library to generate a summary and interesting facts about a LinkedIn profile.
It performs the following steps:

1. Loads environment variables from a .env file.
2. Configures the AzureChatOpenAI model for generating responses using settings from the config.
3. Defines a prompt template for generating the summary and interesting facts.
4. Scrapes LinkedIn profile data using a third-party library.
5. Converts the scraped data to a string format.
6. Constructs a prompt for the AzureChatOpenAI model.
7. Invokes the AzureChatOpenAI model with the constructed prompt.
8. Handles the response and prints the generated output.

Dependencies:
- langchain
- dotenv
- third_parties.linkedin (for scraping LinkedIn profile data)
"""

from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from third_parties.linkedin import scrape_linkedin_profile
import os
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


# Initialize the AzureChatOpenAI model using settings from the config
model = AzureChatOpenAI(
    azure_endpoint=config["azure_endpoint"],  # Azure endpoint
    openai_api_key=config["api_key"],  # Azure API key
    azure_deployment=config["model_name"],  # Deployment name
    openai_api_version=config["api_version"],  # API version
    temperature=0,
    default_headers=headers
)

if __name__ == "__main__":
    print('Hello LangChain!')

    summary_template = """
    Given the LinkedIn information {information} about a person, I want you to create:
    1. A short summary of the person's profile.
    2. Two interesting facts about the person with pointers as "-" under a section titled "Interesting Facts". Create this section only if there are facts.
    """

    summary_prompt_template = PromptTemplate(
        input_variables=['information'],
        template=summary_template
    )

    linkedin_data = scrape_linkedin_profile(
        "https://www.linkedin.com/in/eden-marco"
    )
    print('Scraped LinkedIn data successfully.')

    # Ensure linkedin_data is a string
    linkedin_data_str = json.dumps(linkedin_data, indent=2) if isinstance(
        linkedin_data, dict) else str(linkedin_data)

    # Construct the prompt
    prompt = summary_prompt_template.format(information=linkedin_data_str)

    # Invoke the model with the constructed prompt
    response = model.invoke([
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": prompt},
    ])

    # Print the output
    print('LLM output:', response.content)
