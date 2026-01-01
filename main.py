import csv
import json
import os
import time

from modules import getCreationByUsername, fetchText, countToken, getDomain

INPUT_CSV = "userTest101.csv"
OUTPUT_DIR = "output"
def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    users_to_process = []

    with open(INPUT_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            if row:
                users_to_process.append(row[0].strip())

    for username in users_to_process:
        json_filename = os.path.join(OUTPUT_DIR, f"{username}.json")
        
        # uncomment to skip existing
        # if os.path.exists(json_filename):
        #     print(f"Skipping {username}, file already exists.")
        #     continue

        metadata_list = getCreationByUsername(username)
        if metadata_list:
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(metadata_list, json_file, indent=4, ensure_ascii=False)
                print(f"Saved {json_filename}")
        else:
            print(f" -> No entries for {username}")
        
        time.sleep(1) # avoid crash (429)

    for filename in os.listdir(OUTPUT_DIR):
        if not filename.endswith(".json"):
            continue
            
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)

        data_modified = False # track for changes

        for entry in articles_data:
            # only fetch if text param not present
            if "text" not in entry:
                revid = entry.get("revid")
                title = entry.get("title")
                entry["text"] = fetchText(revid)
                entry["token_count"] = countToken(entry.get("text", ""))
                topics = getDomain(title)
                if topics:
                    entry["domain"] = topics
                else:
                    entry["domain"] = "Unknown"
                
                print(f" -> Processed {entry['title']} (Tokens: {entry['token_count']})")
                data_modified = True
                
                time.sleep(1) # Rate limiting
        if data_modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()