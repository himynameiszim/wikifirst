import requests
import json

# from getCreationByUsername import getCreationByUsername

def fetchBatchText(rev_ids):
    if not rev_ids:
        return {}
    
    url = "https://en.wikipedia.org/w/api.php"
    headers = { "User-Agent": "Wikifirst/1.0 (s1312004@u-aizu.ac.jp)" }
    
    revids_str = "|".join(str(r) for r in rev_ids)
    
    # Switch to POST to avoid "414 URI Too Long" errors
    # POST requests carry data in the body, not the URL.
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "revids": revids_str,
        "rvprop": "content|ids",
        "rvslots": "main"
    }
    
    results = {}
    try:
        # CHANGE: Use POST instead of GET for batching
        response = requests.post(url, data=params, headers=headers)
        
        # 1. Check if the request was actually successful
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text[:200]}...") # Print first 200 chars of error
            return {}

        # 2. Try to parse JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Error: API returned invalid JSON.")
            print(f"Raw Response: {response.text[:500]}") # Crucial for debugging
            return {}
        
        # 3. Process Data
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "revisions" in page_data:
                for rev in page_data["revisions"]:
                    revid = rev["revid"]
                    try:
                        text = rev["slots"]["main"]["*"]
                        results[revid] = text
                    except KeyError:
                        results[revid] = "" 
                        
    except Exception as e:
        print(f"Batch request failed: {e}")
        
    return results

# def main():
#     _, rev_ids = getCreationByUsername("Europe22") # Get revision IDs for a user
#     texts = fetch_text_batch(rev_ids)
#     for revid, text in texts.items():
#         print(f"Revision ID: {revid}\nText: {text[:100]}...\n") # Print first 100 chars
#     print(rev_ids)

# main()