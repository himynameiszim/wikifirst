import requests
import time

def getArticlesbyUser(username, createdOnlyFlag=True):
    """
    :param
        username: username to be fetched
        createdOnlyFlag: True -> articles created by user (set by default)
                        False -> articles created/edited by user
    :return
        list of articles fetched
    """
    titles = set() # avoid editting duplicates

    # raw API
    url = "https://en.wikipedia.org/w/api.php"

    HEADERS = {
        "User-Agent": "Wikifirst/1.0 (s1312004@u-aizu.ac.jp)"
    }

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "ucuser": username,
        "uclimit": 500, #subject to change if needed
        "ucnamespace": 0 # Wikipedia's namespace definition: https://en.wikipedia.org/wiki/Wikipedia:Namespace
    }

    if createdOnlyFlag:
        PARAMS["ucshow"] = "new"

    while True:
        try:
            response = requests.get(url, params=PARAMS, headers=HEADERS).json() # added headers to avoid 403 (idk why)

            if "query" in response and "usercontribs" in response["query"]: # check if there are contributions
                for contrib in response["query"]["usercontribs"]: 
                    titles.add(contrib["title"])
            if "continue" in response:
                PARAMS.update(response["continue"]) 
            else:
                break

            time.sleep(1) # avoid crash (429)
        except Exception as e:
            print(f"Some error here: {e}")
            break

    print(f"Fetched {len(titles)} articles from {username}")
    print("-----")
    print(titles[:50])

    return list(titles)

# random test
# def main():
#     getArticlesbyUser("Europe22", createdOnlyFlag=True)
#     getArticlesbyUser("Ilwilson", createdOnlyFlag=False)

# if __name__ == "__main__":
#     main()