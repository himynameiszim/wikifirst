import requests
from bs4 import BeautifulSoup
import time

from cleanRawHTML import cleanRawHTML

# global var, add to main script
# raw API
url = "https://en.wikipedia.org/w/api.php"
HEADERS = { "User-Agent": "Wikifirst/1.0 (s1312004@u-aizu.ac.jp)" }

def fetchOldText(revID):
    """
    Fetches text from a given revision ID.
    :param
        revID: revision ID to be fetched
    :return
        text
    """
    PARAMS = {
        "action": "parse",
        "format": "json",
        "oldid": revID,
        "prop": "text"
    }
    try:
        print(f"Fetching text for revision ID: {revID}.")
        data = requests.get(url, params=PARAMS, headers=HEADERS).json()
        raw_html = data["parse"]["text"]["*"]
        
        cleanText = cleanRawHTML(raw_html)
        return cleanText
    except Exception as e:
        return f"Error fetching text: {e}"
    
# random test
def main():
    Wilson_revID = 130042734
    testText = fetchOldText(Wilson_revID)
    print(testText)

if __name__ == "__main__":
    main()