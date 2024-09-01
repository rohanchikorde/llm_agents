"""
This script uses the LangChain library to generate a summary and interesting facts about a LinkedIn profile.
It performs the following steps:

1. Loads environment variables from a .env file.
2. Configures API settings and headers for making requests to the Azure OpenAI endpoint.
3. Defines a prompt template for generating the summary and interesting facts.
4. Scrapes LinkedIn profile data using a third-party library.
5. Converts the scraped data to a string format.
6. Constructs messages for the OpenAI API request.
7. Initializes the AzureChatOpenAI client with the configured settings.
8. Creates an LLMChain with the prompt template and AzureChatOpenAI client.
9. Invokes the chain with the LinkedIn data to generate the summary and interesting facts.
10. Prints the generated output.

Dependencies:
- langchain
- dotenv
- requests
- json
- third_parties.linkedin (for scraping LinkedIn profile data)
"""
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from third_parties.linkedin import scrape_linkedin_profile
import os
import requests
import json
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

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

# Headers for the API request
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": config["api_key"],
}


def ice_break_with(name: str) -> str:
    """
    Generates a summary and interesting facts about a LinkedIn profile.

    Args:
        name (str): The name of the person whose LinkedIn profile is to be summarized.

    Returns:
        str: The generated summary and interesting facts.
    """
    # Lookup LinkedIn username using the provided name
    linkedin_username = linkedin_lookup_agent(name=name)

    # Scrape LinkedIn profile data
    linkedin_data = scrape_linkedin_profile(linkedin_username, mock=True)

    # Define the prompt template for generating the summary and interesting facts
    summary_template = """
    given the Linkedin information {information} about a person, I want you to create a :
    1. A short summary of the person's profile
    2. two interesting facts about the person with pointers as "-" with title as "Interesting Facts" section. Create a section only if there are facts.
    """

    summary_prompt_template = PromptTemplate(
        input_variables=['information'],
        template=summary_template
    )

    # Initialize the AzureChatOpenAI client
    llm = AzureChatOpenAI(
        azure_endpoint=config["azure_endpoint"],  # Azure endpoint
        openai_api_key=config["api_key"],  # Azure API key
        azure_deployment=config["model_name"],  # Deployment name
        openai_api_version=config["api_version"],  # API version
        temperature=0,
        default_headers=headers
    )

    # Create an LLMChain with the prompt template and AzureChatOpenAI client
    chain = LLMChain(
        llm=llm,
        prompt=summary_prompt_template
    )

    # Invoke the chain with the LinkedIn data to generate the summary and interesting facts
    res = chain.invoke(input={"information": linkedin_data})

    # Print the generated output
    print(res)


if __name__ == "__main__":
    print('LLM Application Launching: Ice Breaker...')
    ice_break_with('Rohan Chikorde Linkedin VP BNYMellon')
