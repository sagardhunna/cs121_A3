import json
import os
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup

stemmer = PorterStemmer()
occurances = dict()

for dirpath, dirnames, filenames in os.walk("developer"): 
    for filename in filenames:
        actual_rel_name = os.path.join(dirpath, filename)
        with open(actual_rel_name,"r") as file:
            jsonObj = json.load(file) 
            soup = BeautifulSoup(jsonObj.get("content"), features="html.parser")
            visible_text = soup.getText(" ").split()
            for text in visible_text:
                text = text.strip()
                occurances
                