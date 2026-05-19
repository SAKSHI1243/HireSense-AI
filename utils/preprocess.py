import re

def clean_text(text):

    # lowercase
    text = text.lower()

    # remove emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # remove urls
    text = re.sub(r'http\S+', ' ', text)

    # remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()