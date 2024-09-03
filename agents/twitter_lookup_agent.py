"""
This script defines a function to look up a Twitter profile URL given a person's name.
It uses the LangChain library to create an agent that interacts with the Azure OpenAI service.
The agent uses a tool to crawl Google for the Twitter profile page URL of the specified person.
"""
import sys
import os
from langchain_openai import AzureChatOpenAI
from langchain import hub
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain_core.tools import Tool
from langchain.prompts.prompt import PromptTemplate
import langchain_openai
from dotenv import load_dotenv
import requests

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.tools import get_profile_url_tavily


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

# Headers for API requests
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": config["api_key"],
}


def lookup(name: str) -> str:
    """
    Look up the Twitter profile URL for a given name.

    Args:
        name (str): The full name of the person.

    Returns:
        str: The Twitter profile URL.
    """
    # Initialize the AzureChatOpenAI client
    llm = AzureChatOpenAI(
        azure_endpoint=config["azure_endpoint"],  # Azure endpoint
        openai_api_key=config["api_key"],  # Azure API key
        azure_deployment=config["model_name"],  # Deployment name
        openai_api_version=config["api_version"],  # API version
        temperature=0,
        default_headers=headers
    )

    # Define the prompt template
    template = """
    given the full name {name_of_person}, I want you to get me a link
    to their Twitter profile page. Your answer should be a valid URL
    and only contain the URL to the Twitter profile.
    """

    prompt_template = PromptTemplate(
        input_variables=['name_of_person'],
        template=template
    )

    # Define the tools for the agent
    tools_for_agent = [
        Tool(
            name="crawl google 4 Twitter profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Twitter profile page URL of a person",
        )
    ]

    # Pull the react prompt from the hub
    react_prompt = hub.pull("hwchase17/react")

    # Create the agent
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )

    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent,
                                   tools=tools_for_agent,
                                   verbose=True)

    # Invoke the agent with the formatted prompt
    result = agent_executor.invoke(
        input={
            "input": prompt_template.format_prompt(name_of_person=name)
        }
    )

    # Extract the Twitter profile URL from the result
    twitter_profile_url = result['output']
    return twitter_profile_url


if __name__ == "__main__":
    print('Hello LangChain!')

    # Example usage
    NAME = "Elon Musk twitter"
    twitter_profile_url = lookup(NAME)
    print(f"Twitter profile URL for {NAME}: {twitter_profile_url}")
