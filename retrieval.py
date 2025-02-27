import os
import re


def find_shortest_list_key(my_map):
    min_length = float('inf')  # Initialize with a large value to ensure first iteration updates
    min_key = None

    for key, list_value in my_map.items():
        if len(list_value) < min_length:
            min_length = len(list_value)
            min_key = key

    return min_key, min_length


# this function is designed to make it more efficient to retrieve which partial index we should use to look for the term
# it will basically check the first word in the file and if the word is larger than the searched word currently at hand
# it adds the document into a map with the word for the designated file,
def find_partial_file(searched_word):
    word_list = searched_word.strip().split(" ")  # splits search into seperate words
    index_map = {}  # map to return

    for word in word_list:  # checks each query word
        first_letter = word[0].lower()
        file_path = f'partial_indexes/index_letter_{first_letter}.txt'

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


def main():
    word = "research uci"
    print(find_partial_file(word))


if __name__ == "__main__":
    main()
