import requests
from bs4 import BeautifulSoup

def get_flux_free_credit():
    url = "https://flux-ai.io/pricing/"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GitHubActionBot/1.0)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Adjust this selector based on real page structure
    free_credit_text = ""
    for elem in soup.find_all(text=True):
        if "free credit" in elem.lower():
            free_credit_text = elem.strip()
            break

    if free_credit_text:
        print(f"Found free credit info: {free_credit_text}")
    else:
        print("Could not find free credit information.")

if __name__ == "__main__":
    get_flux_free_credit()
