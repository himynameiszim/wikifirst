import ollama

def getDomain(text):
    """
    Classifies text into one of 8 categories.
    """
    
    categories = [
        "Hard-Pure-Life (e.g., Botany, Zoology)",
        "Hard-Pure-Nonlife (e.g., Physics, Chemistry)",
        "Hard-Applied-Life (e.g., Medicine, Agriculture)",
        "Hard-Applied-Nonlife (e.g., Engineering, Economics)", 
        "Soft-Pure-Life (e.g., Psychology, Anthropology)",
        "Soft-Pure-Nonlife (e.g., Computer Science, History)",
        "Soft-Applied-Life (e.g., Education)",
        "Soft-Applied-Nonlife (e.g., Business, Law)"
    ]

    prompt = f"""
    You are an expert academic classifier using the Biglan Model. 
    Classify the given text into EXACTLY one of these 8 categories:
    {', '.join(categories)}

    Use these specific definitions based on the user's framework:
    - **Hard vs Soft**: 'Hard' has high consensus/math (e.g., Physics, Economics). 'Soft' has lower consensus/more interpretation (e.g., Business, Computer Science).
    - **Pure vs Applied**: 'Pure' is abstract/theoretical. 'Applied' is practical/vocational.
    - **Life vs Non-life**: Dealing with living organisms vs. non-living systems.

    Return ONLY the category name. NO NEED FOR EXPLANATION.
    """

    try:
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'system',
                'content': prompt,
            },
            {
                'role': 'user',
                'content': f"Title to classify: \"{text}\"\n\nCategory:",
            },
        ])
        label = response['message']['content'].strip()
                
        return label
        
    except Exception as e:
        print(f"some error: {e}")
        return "NA"