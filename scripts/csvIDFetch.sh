#!/bin/bash

# Input and Output files
CSV_FILE="users.csv"
JSON_FILE="wikipedia_users.json"

# Start the JSON array
echo "[" > "$JSON_FILE"

# Initialize a flag to handle commas between JSON objects
IS_FIRST=true

# Read the file line by line
# 'tail -n +2' skips the first header row
# 'IFS=,' tells the read command to split by comma
# 'read -r username remainder' reads the first column into 'username' and throws everything else (like ,,,) into 'remainder'
tail -n +2 "$CSV_FILE" | while IFS=, read -r username remainder || [ -n "$username" ]; do

    # Remove potential Windows carriage return characters (\r) and surrounding quotes
    username=$(echo "$username" | tr -d '\r"')

    # Skip empty lines
    if [ -z "$username" ]; then
        continue
    fi

    # If this is not the first item, print a comma to separate objects
    if [ "$IS_FIRST" = true ]; then
        IS_FIRST=false
    else
        echo "," >> "$JSON_FILE"
    fi

    # Construct the Wikipedia URL
    # ${username// /_} replaces all spaces with underscores
    URL_USERNAME="${username// /_}"
    URL="https://en.wikipedia.org/wiki/User:$URL_USERNAME"

    # Escape double quotes in the username for JSON safety
    SAFE_USERNAME="${username//\"/\\\"}"

    # Write the JSON object
    echo "    {" >> "$JSON_FILE"
    echo "        \"username\": \"$SAFE_USERNAME\"," >> "$JSON_FILE"
    echo "        \"url\": \"$URL\"" >> "$JSON_FILE"
    echo -n "    }" >> "$JSON_FILE"

done

# Close the JSON array
echo "" >> "$JSON_FILE"
echo "]" >> "$JSON_FILE"

echo "Done! Generated $JSON_FILE"
