import requests
import ollama

url = "https://en.wikipedia.org/w/api.php"
HEADERS = { "User-Agent": "Wikifirst/1.0 (s1312004@u-aizu.ac.jp)" }

def get_article_categories(title):
    """
    Fetches the list of visible categories for a given Wikipedia article title.
    """
    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "categories",
        "titles": title,
        "cllimit": 500,      
        "clshow": "!hidden"   
    }

    try:
        response = requests.get(url, params=PARAMS, headers=HEADERS).json()
        pages = response.get("query", {}).get("pages", {})
        
        for page_id, page_data in pages.items():
            if "categories" in page_data:
                # Extract just the title, removing "Category:" prefix
                return [c["title"].replace("Category:", "") for c in page_data["categories"]]
            else:
                return []
                
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return []

# --- 2. THE UPDATED OLLAMA FUNCTION ---

def map_categories_to_main_topic(specific_categories):
    """
    Uses Ollama to map a list of specific Wikipedia categories to top-level domains.
    """
    
    if not specific_categories:
        return "NA"

    main_categories = [
        "General reference",
        "Culture and the arts",
        "Geography and places",
        "Health and fitness",
        "History and events",
        "Human activities",
        "Mathematics and logic",
        "Natural and physical sciences",
        "People and self",
        "Philosophy and thinking",
        "Religion and belief systems",
        "Society and social sciences",
        "Technology and applied sciences"
    ]

    cat_string = ", ".join(specific_categories)

    system_instruction = f"""
    You are a Wikipedia ontology expert.
    I will provide a list of specific categories tags for an article.
    You must map this article to EXACTLY one of these 12 top-level domains:
    {', '.join(main_categories)}

    STRICT RULES:
    1. Return ONLY the top-level category name.
    2. If the tags describe a person (e.g. "Living people", "Alumni"), look at their FIELD of work (e.g. "Physicists" -> "Natural and physical sciences").
    3. If the tags are mixed, pick the most dominant academic or professional field.
    """

    try:
        response = ollama.chat(model='phi3', messages=[
            {
                'role': 'system',
                'content': system_instruction,
            },
            {
                'role': 'user',
                'content': f"Specific Categories: [{cat_string}]\n\nTop-Level Domain:",
            },
        ])
        
        # Clean output
        predicted = response['message']['content'].strip()
        
        # Simple validation
        for main_cat in main_categories:
            if main_cat.lower() in predicted.lower():
                return main_cat
                
        return "NA"

    except Exception as e:
        print(f"Ollama Error: {e}")
        return "Error"
