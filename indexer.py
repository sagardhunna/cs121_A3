import json
import os
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from tokenizeAndStem import tokenize
from collections import OrderedDict, defaultdict
import re

stemmer = PorterStemmer()
file_number = 0
partial_index_num = 1
unique_keys = 0
token_map = defaultdict(list)
url_map = {}


# creates partial index file and overwrites token_map and file_number


def create_partial_index():
    global file_number, partial_index_num, unique_keys, token_map

    # ensures the directory is present
    os.makedirs("rough_indexes", exist_ok=True)

    token_map = OrderedDict(sorted(token_map.items()))  # Sort tokens
    file = open(f"rough_indexes/rough_ind_{partial_index_num}.txt", 'w') 
    
    for key in token_map.keys():
        first_letter = key[0].lower()  # Normalize to lowercase
        if first_letter not in 'abcdefghijklmnopqrstuvwxyz0123456789':
            continue  # skips bad stuff here ^^         this shouldnt be needed tho? assuming tokenizer is working correctly
        # write in the values onto the letter docs
        file.write(f'{key}')
        for item in token_map[key]:
            for doc, freq in item.items():
                file.write(f' {doc},{freq}')
        file.write('\n')
    file.close()
        
    unique_keys += len(token_map.keys())
    token_map.clear()
    partial_index_num += 1


# {word: [(doc#, freq)]}
# map with key = token and value being a set of tuples (doc, frequency)

def create_id_url():
    global url_map
    existing_ids = set()

    # read IDs to prevent duplicates if already there
    if os.path.exists("url_id.txt"):
        with open("url_id.txt", "r") as file:
            for line in file:
                existing_ids.add(line.split(":")[0])  # Store existing IDs

    # append new IDs
    with open("url_id.txt", "a") as file:
        for idNum, url in url_map.items():
            if str(idNum) not in existing_ids:
                file.write(f'{idNum}:{url}\n')

    url_map.clear()


def process_file(file_path):
    global file_number, token_map, url_map
    with open(file_path, "r") as file:
        # IMPLEMENT WEIGHTS OF IMPORTANCE FOR H1/H2/H3
        jsonObj = json.load(file)
        soup = BeautifulSoup(jsonObj.get("content"), features="html.parser")
        visible_text = soup.getText(" ")
        doc_name = "doc" + str(file_number + 1)
        tokenize(visible_text, doc_name, token_map, stemmer)
        file_number += 1
        url_map[file_number] = jsonObj.get("url")
        print(f"going through document: {doc_name} (current token map size: {len(token_map.keys())})")
        if file_number % 2500 == 0: # partializing it
            create_partial_index()
            create_id_url()
            print("Making index and clearing map")
            # exit() #for testing
            return

def create_total_count():
    global file_number
    if os.path.exists("url_id.txt"):
        with open("url_id.txt", "r") as file:
            for line in file:
                pass
            id_line = re.match(r"(\d+):", line)
            total_num = id_line.group(1)
            print(total_num)
            with open("total_count.txt", "w") as file:
                file.write(f'{total_num}')
            file.close()
    else:
        with open("total_count.txt", "w") as file:
            file.write(f'{file_number}')
        file.close()

def main():
    global unique_keys

    # for dirpath, dirnames, filenames in os.walk("developer"):
    #     for filename in filenames:
    #         actual_rel_name = os.path.join(dirpath, filename)
    #         if '.json' not in actual_rel_name:
    #             continue
    #         process_file(actual_rel_name) # this will make a rough draft, we will need to compartmentalize and index
    #
    # create_partial_index() # run 1 last time to clear any remaining tokens out of the hashmap that we didn't hit 2500 files to partialize
    # create_id_url()
    create_total_count()  # this basically prints out the total file number
    # print("Making final index")
    # print(f'Token Unique Tokens: {unique_keys}')
    # print(f'Total file size: {((os.path.getsize("partial_indexes/partial_index_1.txt") + os.path.getsize("partial_indexes/partial_index_2.txt") + os.path.getsize("partial_indexes/partial_index_3.txt")) / 1000)} KB')


if __name__ == "__main__":
    main()
