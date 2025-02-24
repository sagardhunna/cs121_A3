import json
import os
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from tokenizeAndStem import tokenize

stemmer = PorterStemmer()
file_number = 0


# {word: [(doc#, freq)]}
# map with key = token and value being a set of tuples (doc, frequency)
def main():
    global stemmer, file_number

    token_map = {}
    for dirpath, dirnames, filenames in os.walk("developer"):
        for filename in filenames:
            actual_rel_name = os.path.join(dirpath, filename)
            if '.json' not in actual_rel_name:
                continue
            print(f'File we are looking at: File #{file_number}')
            with open(actual_rel_name,"r") as file:
                jsonObj = json.load(file) 
                soup = BeautifulSoup(jsonObj.get("content"), features="html.parser")
                visible_text = soup.getText(" ")
                doc_name = "doc" + str(file_number + 1)
                tokenize(visible_text, doc_name, token_map)
                file_number += 1
                # visible_text is a list of all tokens in file


    with open('testing.txt', 'w') as f:
        for key, value in token_map.items():
            f.write(f'{key}')
            for item in value:
                for key, value in item.items():
                    f.write(f' {key},{value}')
            f.write('\n')
        
    f.close()

    print(f'Docs indexed: {file_number}')
    print(f'Token Unique Tokens: {len(token_map.keys())}')
    print(f'Testing.txt file size: {os.path.getsize("testing.txt")}')


if __name__ == "__main__":
    main()
