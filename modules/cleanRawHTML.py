from bs4 import BeautifulSoup
import re

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
    ignore_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'dl']
    
    for element in soup.find_all(ignore_tags):
        text = element.get_text(strip=True, separator=" ")
        text = re.sub(r'\s+', ' ', text)

        if not text:
            continue
            
        # stop at footers
        if element.name in ['h2', 'h3'] and text in ['External links', 'References', 'See also', 'Notes', 'Bibliography']:
            break
            
        text_blocks.append(text)
    return "\n\n".join(text_blocks)