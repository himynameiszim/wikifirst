from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def getDomain(text):
    """
    :param
        text: input str
    :return
        domain label
    """
    candidate_labels = ["Natural Science", "Social Science"]
    result = classifier(text, candidate_labels)
    return result["labels"][0]