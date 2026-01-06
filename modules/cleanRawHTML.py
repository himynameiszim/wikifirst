from bs4 import BeautifulSoup
import re
import json
import os

def cleanRawHTML(raw_html):
    """
    Parses raw Wikipedia HTML and clean.
    Removes: [edit] buttons, references [1], and footer sections (External links, etc).
    """
    if not raw_html:
        return ""

    soup = BeautifulSoup(raw_html, "html.parser")

    # remove [edit] buttons
    for tag in soup.find_all(class_="mw-editsection"):
        tag.decompose()
        
    # remove reference markers 
    for tag in soup.find_all("sup", class_="reference"):
        tag.decompose()
    
    # remove tables
    for tag in soup.find_all("table"):
        tag.decompose()

    text_blocks = []

    # ignores navigation bars, sidebars, and hidden metadata
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'dl']
    
    for element in soup.find_all(tags):
        text = element.get_text(strip=True, separator=" ")
        text = re.sub(r'\s+', ' ', text)

        if not text:
            continue
            
        # stop at footers
        if element.name in ['h2', 'h3'] and text in ['External links', 'References', 'See also', 'Notes', 'Bibliography']:
            break

        if element.name.startswith("h"):
            continue #ignore headers titles
            
        text_blocks.append(text)
    return "\n\n".join(text_blocks)

# clean output
def main():
    input_dir = r"D:\wikifirst\wikifirst\output"
    output_dir = r"D:\wikifirst\wikifirst\cleaned_output"

    # ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)

        for entry in data:
            entry["text"] = cleanRawHTML(entry["text"])

        save_path = os.path.join(output_dir, filename)
        with open(save_path, 'w', encoding='utf-8') as f_out:
            json.dump(data, f_out, indent=4, ensure_ascii=False)

main()
