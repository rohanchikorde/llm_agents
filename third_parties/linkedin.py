import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from a linkedin profile
       Manually scrape the information from the linkedin profile
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {
            "Authorization": f"Bearer {os.getenv('PROXYCURL_API_KEY')}"
        }
        response = requests.get(
            api_endpoint,
            headers=header_dic,
            params={"url": linkedin_profile_url},
            timeout=10,
        )

    data = response.json()
    print(data)
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(scrape_linkedin_profile("https://www.linkedin.com/in/eden-marco"),
          mock=True)
