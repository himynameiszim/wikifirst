import requests
import time
import json

# global var, add to main script
# raw API
url = "https://en.wikipedia.org/w/api.php"
HEADERS = { "User-Agent": "Wikifirst/1.0 (s1312004@u-aizu.ac.jp)" }

def getCreationByUsername(username, createdOnlyFlag=True):
    """
    Fetches the titles and initial revision ID for all articles created by username.
    :param
        username: username to be fetched
        createdOnlyFlag: True -> articles created by user (set by default)
                        False -> articles created/edited by user
    :return
        list of tuples (title, revID) fetched
    """
    creations = []
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "ucuser": username,
        "uclimit": 500, # subject to change if needed
        "ucnamespace": 0, # Wikipedia's namespace definition: https://en.wikipedia.org/wiki/Wikipedia:Namespace
        "ucprop": "ids|title|timestamp" # fetch revision IDs, titles, and timestamps
    }

    if createdOnlyFlag:
        PARAMS["ucshow"] = "new" # only fetch created articles not edits

    print(f"Fetching metadata for {username}")

    while True:
        try:
            response = requests.get(url, params=PARAMS, headers=HEADERS).json()

            if "query" in response and "usercontribs" in response["query"]:
                for contrib in response["query"]["usercontribs"]:
                    creations.append({
                        "title": contrib["title"],
                        "revid": contrib["revid"], # points to the text at creation
                        "date": contrib["timestamp"]
                    })
            
            if "continue" in response:
                PARAMS.update(response["continue"])
            else:
                break

            time.sleep(1) # avoid crash (429)
            
        except Exception as e:
            print(f"Some error: {e}")
            break

    print(f"Found {len(creations)} created articles by {username}.")
    print("-----")
    print(creations[:5])

    # print("Saving creations to JSON.")
    # output = f"{username}_creations.json"
    # with open(output, "w", encoding="utf-8") as f:
    #     json.dump(creations, f, indent=4, ensure_ascii=False)
    # print(f"Saved {output}.")

    return creations

# # random test
# def main():
#     getCreationByUsername("Europe22", createdOnlyFlag=True)
#     getCreationByUsername("Ilwilson", createdOnlyFlag=True)

# if __name__ == "__main__":
#     main()