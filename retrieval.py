import re
from nltk.stem import PorterStemmer
import os

# Get the absolute path to the root CS121 directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # CS121

# Construct the absolute path to partial_indexes folder
PARTIAL_INDEXES_DIR = os.path.join(ROOT_DIR, "partial_indexes")

def find_shortest_list_key(my_map):
    min_length = float('inf')  # Initialize with a large value to ensure first iteration updates
    min_key = None

    for key, list_value in my_map.items():
        if len(list_value) < min_length:
            min_length = len(list_value)
            min_key = key

    return min_key, min_length


# this function is designed to make it more efficient to retrieve which partial index we should use to look for the term
# it will basically check the first letter in the word and search the document that matches that letter
def find_partial_file(searched_word):
    stemmer = PorterStemmer()

    searched_word = searched_word.lower()
    word_list = searched_word.strip().split(" ")  # splits search into seperate words

    index_map = {}  # map to return

    for word in word_list:  # checks each query word
        word = stemmer.stem(word.lower())
        first_letter = word[0].lower()
        file_path = f'{PARTIAL_INDEXES_DIR}/partial_index_{first_letter}.txt'

        with open(file_path, "r") as file:
            for line in file:
                if line:
                    words = line.split()
                    first_word = words[0]

                if first_word == word:
                    doc_ids = re.findall(r'doc(\d+)', line)
                    index_map[word] = set(int(doc_id) for doc_id in doc_ids)
                    break
                    # print(index_map)

    # Ensure all words have at least one match before performing intersection
    if len(index_map) != len(word_list):
        return set()  # If any word is missing, return an empty set

    # Perform intersection to find common document IDs
    common_doc_ids = set.intersection(*index_map.values())

    return common_doc_ids


def findURL(list_of_matches):
    list_of_matches = set(map(int, list_of_matches))  # Convert all to int
    list_of_url = set()  # Use set to avoid duplicates

    with open(f'{ROOT_DIR}/url_id.txt', "r") as file:
        for line in file:
            id_line = re.match(r"(\d+):(.+)", line)
            id_value = id_line.group(1)
            link = str(id_line.group(2))

            if int(id_value) in list_of_matches:
                # print(f'This is working: {id_value}')
                list_of_url.add(link)  # Avoid duplicate URLs

    return list(list_of_url)  # Convert back to a list

def makeQuery(query):
    matched_ids = find_partial_file(query)
    top_5 = []
    count = 0

    for links in findURL(matched_ids):
        if count == 5:
                break
        top_5.append(links)
        count += 1    
    
    return top_5


def main():
    for i in range(4):
        word = input("Please enter a search query: ")

        matched_ids = find_partial_file(word)
        # print("Here are the overlapping strings: ")
        # print(matched_ids)
        count = 0
        for links in findURL(matched_ids):
            if count == 5:
                break
            print(links)
            count += 1


if __name__ == "__main__":
    main()
