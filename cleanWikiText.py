import re
import string
import mwparserfromhell
import os
import json

def rm_refs(x):
    REF_RE = '<ref([-\w=" <>]+)?>.*?<([ ]+)?\/([ ]+)?ref>'
    x = re.sub(REF_RE, ' ', x)
    # leading </ref>
    if '</ref>' in x:
        x = re.sub(REF_RE, ' ', '<ref>' + x)
    # trailing <ref>
    if '<ref' in x:
        x = re.sub(REF_RE, ' ', x + '</ref>')
    return x
    
def clean_wikitext(token_list):    
    if isinstance(token_list, list):
        x = ' '.join(token_list)
    else:
        x = token_list

    # ascii only
    x = ''.join(filter(lambda x: x in string.printable, x))

    # preemptively remove <ref>'s (including uncompleted)
    x = x.strip()
    x = rm_refs(x)
    # collapse multispaces
    x = re.sub('[ ]+', ' ', x)

    parse = mwparserfromhell.parse(x)
    plaintext = parse.strip_code()
    plaintext = rm_refs(plaintext) # get refs again? some things missed
    # collapse multispaces
    plaintext = re.sub('[ ]+', ' ', plaintext)
    # parse again to hit complicatd nested wikicode like 21055249
    parse = mwparserfromhell.parse(plaintext)
    plaintext = parse.strip_code()

    # ignore lines starting with ! or | (likely table artifacts)
    if plaintext.startswith('?') or plaintext.startswith('|'):
        plaintext = ''

    # ignore lines without text, e.g. ( , , , , ) or ]]
    if not re.findall('\w', plaintext):
        plaintext = ''

    # parse AGAIN again to hit remaining links e.g. 377258469
    plaintext = plaintext.replace('[ ', '[').replace(' ]', ']')
    parse = mwparserfromhell.parse(plaintext)
    plaintext = parse.strip_code()

    # at this point just rm all brackets
    plaintext = plaintext.replace(']', '').replace('[', '')
    # rm html
    plaintext = re.sub('http\S+', '', plaintext)
    # rm parents with nothing in them, e.g. (; )
    plaintext = re.sub('\([^\w]*\)', '', plaintext)
    # rm remining <del>, <ins> (valid tags should already have been taken parsed)
    plaintext = re.sub('<\/?(del|ins)([-\w=" <>]+)?>', '', plaintext)
    # fuck stars
    plaintext = plaintext.replace('*', '')
    # rm table fragments
    plaintext = re.sub('(right[ ]?\||left[ ]?\||thumb[ ]?\||frame[ ]?\||\d+px[ ]?\|)', '', plaintext)
    # ignore timestamp sentences
    if 'retrieved on' in plaintext.lower():
        plaintext = ''
    # msc html missed
    plaintext = plaintext.replace('<blockquote>', '')
    
    # remove tabs and newlines (those is our deliminators beeyotch)
    plaintext = plaintext.replace('\t', '')
    plaintext = plaintext.replace('\n', '')
    plaintext = plaintext.replace('\r', '')
    # collapse multispaces (again again)
    plaintext = re.sub('[ ]+', ' ', plaintext).strip()
    
    return plaintext

def main():
    input_dir = r"D:\wikifirst\wikifirst\output"
    output_dir = r"D:\wikifirst\wikifirst\cleaned_output"

    # ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)

        for entry in data:
            entry["text"] = clean_wikitext(entry["text"])

        save_path = os.path.join(output_dir, filename)
        with open(save_path, 'w', encoding='utf-8') as f_out:
            json.dump(data, f_out, indent=4, ensure_ascii=False)

main()