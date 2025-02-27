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
token_map = {}

# creates partial index file and overwrites token_map and file_number 
def create_partial_index():
    global file_number, total_file_number, partial_index_num, unique_keys, token_map

    # ensures the directory is present
    os.makedirs("partial_indexes", exist_ok=True)

    token_map = OrderedDict(sorted(token_map.items()))  # Sort tokens
    file_handles = {}  # dictionary to manage all letters a-b and numbers 0-9 hopefully

    for key in token_map.keys():
        first_letter = key[0].lower()  # Normalize to lowercase
        if first_letter not in 'abcdefghijklmnopqrstuvwxyz0123456789':
            continue  # skips bad stuff here ^^

        file_path = f"partial_indexes/index_letter_{first_letter}.txt" # this is the path that will be used

        # Open the file in append mode ('a') to avoid overwriting
        if first_letter not in file_handles:
            file_handles[first_letter] = open(file_path, 'a')  # the value of f that will be used to write

        f = file_handles[first_letter]  # get ^ open value up here

        # write in the values onto the letter docs
        f.write(f'{key}')
        for item in token_map[key]:
            for doc, freq in item.items():
                f.write(f' {doc},{freq}')
        f.write('\n')

    # Close all file handles
    for f in file_handles.values():
        f.close()
    total_file_number += file_number
    file_number = 0
    unique_keys += len(token_map.keys())
    token_map.clear()
    partial_index_num += 1

# {word: [(doc#, freq)]}
# map with key = token and value being a set of tuples (doc, frequency)
def main():
    global stemmer, file_number, total_file_number, partial_index_num, unique_keys, token_map

    #token_map = {}
    for dirpath, dirnames, filenames in os.walk("developer"):
        for filename in filenames:
            actual_rel_name = os.path.join(dirpath, filename)
            if '.json' not in actual_rel_name:
                continue
            print(f'File we are looking at: File #{file_number}')
            with open(actual_rel_name,"r") as file:
                # IMPLEMENT WEIGHTS OF IMPORTANCE FOR H1/H2/H3
                jsonObj = json.load(file) 
                soup = BeautifulSoup(jsonObj.get("content"), features="html.parser")
                visible_text = soup.getText(" ")
                doc_name = "doc" + str(total_file_number + 1)
                tokenize(visible_text, doc_name, token_map, stemmer)
                file_number += 1
                # total_file_number += 1
                # visible_text is a list of all tokens in file
            if file_number == 1000:
                '''
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
                total_file_number += file_number
                file_number = 0
                unique_keys += len(token_map.keys())
                token_map.clear()
                partial_index_num += 1
                '''
                # file_path = 'partial_indexes/partial_index_' + str(partial_index_num) + '.txt'
                create_partial_index()
                token_map.clear()
                return


    '''
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
    '''
    # file_path = 'partial_indexes/partial_index_' + str(partial_index_num) + '.txt'
    create_partial_index()

    print(f'Docs indexed: {total_file_number}')
    print(f'Token Unique Tokens: {unique_keys}')
    # print(f'Total file size: {((os.path.getsize("partial_indexes/partial_index_1.txt") + os.path.getsize("partial_indexes/partial_index_2.txt") + os.path.getsize("partial_indexes/partial_index_3.txt")) / 1000)} KB')


if __name__ == "__main__":
    main()
