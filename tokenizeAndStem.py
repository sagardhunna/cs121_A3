# tokenize + stem to create a list of tokens that are stemmed words and also only alphanumeric words

import json
import os
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import re

stemmer = PorterStemmer()
'''
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
'''

def tokenize(visible_text, doc_name): # takes in a file path and returns a List<Token>
    delimiters = r"[^a-zA-Z]" 
    token_map = {}
    '''
    {
        word: set({
            doc_name: word_freq
        })
    }
    '''
    
    some_tokens = re.split(delimiters, visible_text)
    for token in some_tokens:
        word = stemmer.stem(token.lower())
        if word in token_map:
            # check if the doc we are in exists in the set at token_map[word]
            


    return token_map



def main():
    with open("developer/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json", 'r') as file:
        jsonObj = json.load(file)
        soup = BeautifulSoup(jsonObj.get("content"), features="html.parser")
        visible_text = soup.getText(" ") # array of all the visible text on a page
        with open('testing.txt', 'w') as f:
            f.write(str(visible_text))
        
        f.close()
    file.close()


if __name__ == "__main__":
    main()