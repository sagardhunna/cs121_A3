import json
import os
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup

stemmer = PorterStemmer()

word_to_doc_freq = {}
# {word: [(doc#, freq)]}
# map with key = token and value being a set of tuples (doc, frequency)
for dirpath, dirnames, filenames in os.walk("developer"):
    for filename in filenames:
        actual_rel_name = os.path.join(dirpath, filename)
        with open(actual_rel_name,"r") as file:
            jsonObj = json.load(file) 
            soup = BeautifulSoup(jsonObj.get("content"), features="html.parser")
            visible_text = soup.getText(" ").split()
            # visible_text is a list of all tokens in file
            for text in visible_text:
                text = text.strip()
                