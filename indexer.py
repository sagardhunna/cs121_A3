import json
import os
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from tokenizeAndStem import tokenize
from collections import OrderedDict


stemmer = PorterStemmer()
file_number = 0
total_file_number = 0
partial_index_num = 1
unique_keys = 0


# {word: [(doc#, freq)]}
# map with key = token and value being a set of tuples (doc, frequency)
def main():
    global stemmer, file_number, total_file_number, partial_index_num, unique_keys

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
                doc_name = "doc" + str(total_file_number + 1)
                tokenize(visible_text, doc_name, token_map)
                file_number += 1
                total_file_number += 1
                # visible_text is a list of all tokens in file
            if file_number == 19000:
                file_path = 'partial_indexes/partial_index_' + str(partial_index_num) + '.txt'
                token_map = OrderedDict(sorted(token_map.items()))
                with open(file_path, 'w') as f:
                    for key, value in token_map.items():
                        f.write(f'{key}')
                        for item in value:
                            for key, value in item.items():
                                f.write(f' {key},{value}')
                        f.write('\n')                
                f.close()
                file_number = 0
                unique_keys += len(token_map.keys())
                token_map.clear()
                partial_index_num += 1

    file_path = 'partial_indexes/partial_index_' + str(partial_index_num) + '.txt'
    token_map = OrderedDict(sorted(token_map.items()))
    with open(file_path, 'w') as f:
        for key, value in token_map.items():
            f.write(f'{key}')
            for item in value:
                for key, value in item.items():
                    f.write(f' {key},{value}')
            f.write('\n')                
    f.close()
    file_number = 0
    unique_keys += len(token_map.keys())
    token_map.clear()

    print(f'Docs indexed: {total_file_number}')
    print(f'Token Unique Tokens: {unique_keys}')
    print(f'Testing.txt file size: {((os.path.getsize("partial_indexes/partial_index_1.txt") + os.path.getsize("partial_indexes/partial_index_2.txt") + os.path.getsize("partial_indexes/partial_index_3.txt")) / 1000)} KB')


if __name__ == "__main__":
    main()
