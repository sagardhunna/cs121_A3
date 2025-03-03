import re
from nltk.stem import PorterStemmer

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
        file_path = f'partial_indexes/partial_index_{first_letter}.txt'

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

    with open("url_id.txt", "r") as file:
        for line in file:
            id_line = line.strip().split(":")
            if len(id_line) < 2:  # Skip malformed lines
                continue
            id_num, url = int(id_line[0]), id_line[1]

            if id_num in list_of_matches:
                list_of_url.add(url)  # Avoid duplicate URLs

    return list(list_of_url)  # Convert back to a list


def main():
    for i in range(4):
        word = input("Please enter a search query: ")

        matched_ids = find_partial_file(word)
        print("Here are the overlapping strings: ")
        print(matched_ids)
        for links in findURL(matched_ids):
            print(links)


if __name__ == "__main__":
    main()
