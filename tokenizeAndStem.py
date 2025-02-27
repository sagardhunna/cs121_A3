# tokenize + stem to create a list of tokens that are stemmed words and also only alphanumeric words

import json
import os
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import re

# TO DO TRY TO USE OrderedDict DATA STRUCTURE INSTEAD OF REGULAR DICT
# MIGHT SAVE US TIME WHEN OUTPUTTING DATA IN A SPECIFIC ORDER


# stemmer is a global variable that is used in tokenize, prevents us from reinitializing it everytime tokenize is called

def tokenize(visible_text, doc_name, token_map, stemmer): # takes in a file path and returns a List<Token>
    delimiters = r"[^a-zA-Z0-9]" 

    '''
    Example of how token_map loooks
    {
        word: [{doc_name: freq1}, {doc_name2: freq}]
    }
    '''

    temp_map = {}
    '''
    Example of how temp_map looks
    {
        word1: freq1,
        word2: freq2
    }'''

    # create a map of word: freq, which we will append to the MAIN TOKEN_MAP at the end after counting frequencies
    some_tokens = re.split(delimiters, visible_text)

    for token in some_tokens:
        if token == "":
            continue
        word = stemmer.stem(token.lower())
        if word in temp_map:
           temp_map[word] += 1
        else:
            temp_map[word] = 1
    
    # using the previous map of words and frequencies, append to our main token_map array of hashes
    # Merge into the global token_map
    for key, value in temp_map.items():
        if key in token_map:
            found = False
            for entry in token_map[key]:
                if doc_name in entry:
                    entry[doc_name] += value  # word was found before
                    found = True
                    break
            if not found:
                token_map[key].append({doc_name: value})
        else:
            token_map[key] = [{doc_name: value}]  # word never found before



def main():

    # testing to make sure our tokenize and stem functionality works with 3 files
    main_path = "developer/aiclub_ics_uci_edu/"
    absolute_path = ["8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json","9a59f63e6facdc3e5fe5aa105c603b545d4145769a107b4dc388312a85cf76d5.json","906c24a2203dd5d6cce210c733c48b336ef58293212218808cf8fb88edcecc3b.json"]
    token_map = {}
    for i in range(len(absolute_path)):
        file_path = main_path + absolute_path[i]
        # the following is beign done in indexer.py, but in indexer.py we just need to call the tokenizer function
        with open(file_path) as file:
            jsonObj = json.load(file)
            soup = BeautifulSoup(jsonObj.get("content"), features="html.parser")
            visible_text = soup.getText(" ") # array of all the visible text on a page
            tokenize(visible_text, f'doc{i}', token_map)
    
    file.close()

    # just testing to make sure everything works correctly
    with open('testing.txt', 'w') as f:
        for key, value in token_map.items():
            f.write(f'{key}')
            for item in value:
                for key, value in item.items():
                    f.write(f' {key},{value}')
            f.write('\n')
        
    f.close()



if __name__ == "__main__":
    main()