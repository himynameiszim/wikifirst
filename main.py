import csv
import json
import os
import time

from modules import getCreationByUsername, fetchText, countToken, getDomain, getCategory, fetchBatchText

INPUT_CSV = "userTest101.csv"
OUTPUT_DIR = "output"
BATCH_SIZE = 50
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
        if os.path.exists(json_filename):
            print(f"Skipping {username}, file already exists.")
            continue

        metadata_list, _ = getCreationByUsername(username)
        if metadata_list:
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(metadata_list, json_file, indent=4, ensure_ascii=False)
                print(f"Saved {json_filename}")
        else:
            print(f" -> No entries for {username}")
        
        time.sleep(1) # avoid crash (429)

    # # old
    # for filename in os.listdir(OUTPUT_DIR):
    #     if not filename.endswith(".json"):
    #         continue
            
    #     filepath = os.path.join(OUTPUT_DIR, filename)

    #     with open(filepath, 'r', encoding='utf-8') as f:
    #         articles_data = json.load(f)

    #     data_modified = False # track for changes

    #     for entry in articles_data:
    #         # only fetch if text param not present
    #         if "text" not in entry:
    #             revid = entry.get("revid")
    #             title = entry.get("title")
    #             entry["text"] = fetchText(revid)
    #             if "Redirect to:" in entry["text"]:
    #                 entry["token_count"] = 0
    #                 entry["domain"] = "System/Redirect"
    #                 entry["text"] = ""
    #                 continue
    #             else:
    #                 entry["token_count"] = countToken(entry.get("text", ""))
    #                 topics = getCategory(title)
    #                 if topics:
    #                     entry["domain"] = topics
    #                 else:
    #                     entry["domain"] = "Unknown"
    #             print(f" -> Processed {entry['title']} (Tokens: {entry['token_count']})")
    #             data_modified = True
                
    #             time.sleep(0.5) # Rate limiting
    #     if data_modified:
    #         with open(filepath, 'w', encoding='utf-8') as f:
    #             json.dump(articles_data, f, indent=4, ensure_ascii=False)


    """New batch fetching"""
    print("\nStarting batch processing of text content...")

    for filename in os.listdir(OUTPUT_DIR):
        if not filename.endswith(".json"):
            continue
            
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)

        data_modified = False 

        # 1. Identify all entries that need processing (missing "text")
        pending_entries = [entry for entry in articles_data if "text" not in entry]

        if pending_entries:
            print(f"Processing {len(pending_entries)} new entries in {filename}...")
            data_modified = True

            # 2. Loop through the pending entries in chunks of BATCH_SIZE
            for i in range(0, len(pending_entries), BATCH_SIZE):
                batch = pending_entries[i : i + BATCH_SIZE]
                
                # Extract revids for this batch
                batch_revids = [entry.get("revid") for entry in batch]
                
                try:
                    # 3. Fetch batch text
                    # Assumption: returns dict { revid: "content" }
                    batch_results = fetchBatchText(batch_revids) 
                except Exception as e:
                    print(f"Error fetching batch for {filename}: {e}")
                    batch_results = {}

                # 4. Update the entries with the fetched results
                for entry in batch:
                    revid = entry.get("revid")
                    title = entry.get("title")
                    
                    # Get text from results, default to empty string if failed
                    # Ensure type matching (str vs int) depending on your API return
                    text_content = batch_results.get(revid) or batch_results.get(str(revid), "")
                    
                    entry["text"] = text_content

                    # Post-processing logic (Same as original)
                    if "Redirect to:" in text_content:
                        entry["token_count"] = 0
                        entry["domain"] = "System/Redirect"
                        entry["text"] = "" # Clear text for redirects if desired
                    else:
                        entry["token_count"] = countToken(text_content)
                        # NOTE: getCategory is likely individual API calls. 
                        # This might still be slow unless getCategory is also batched or offline.
                        topics = getCategory(title) 
                        if topics:
                            entry["domain"] = topics
                        else:
                            entry["domain"] = "Unknown"
                
                print(f" -> Processed batch {i//BATCH_SIZE + 1} ({len(batch)} items)")
                
                # Rate limiting is now applied per batch, not per article
                time.sleep(1) 

        if data_modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, indent=4, ensure_ascii=False)
            print(f"Updated {filename}")
if __name__ == "__main__":
    main()