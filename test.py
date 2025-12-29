import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='Wikifirst/1.0 (s1312004@u-aizu.ac.jp)'
)

page_test = wiki.page('Ian_Wilson_(phonetician)')

if page_test.exists():
    ### full text : page_test.text
    ### summary : page_test.summary
    ### tittle : page_test.title
    print("Some info about Prof.Wilson: " + page_test.text)
else:
    print("Page does not exist.")
