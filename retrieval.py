import re
from nltk.stem import PorterStemmer
import os
import indexer
import math
from collections import defaultdict

# Get the absolute path to the root CS121 directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # CS121

# Construct the absolute path to partial_indexes folder
PARTIAL_INDEXES_DIR = os.path.join(ROOT_DIR, "partial_indexes")


def doc_count():
    count = 0
    with open(f'{ROOT_DIR}/url_id.txt', "r") as file:
        for line in file:
            count += 1

    return count


total_doc_number = doc_count()


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

    word_doc_freq = {}
    refined_map = {}  # this will have a map that contains word: {docID: score}

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
                    # Here is where we should place our ranking and calculations for tf-idf
                    doc_id_tf = re.findall(r'doc(\d+),(\d+)', line)  # first we extract the frequency and id num
                    word_doc_freq[word] = len(doc_id_tf)  # the length of the list in the word is the doc freq

                    # print(f"Extracted (doc_id, tf) for {word}: {doc_id_tf}")

                    id_tf_word_map = {}  # this map will be added to an ultimate map where we can sum words together
                    for idNum, word_freq in doc_id_tf:
                        tf = int(word_freq)  # this is the frequency of the term in the doc
                        docID = int(idNum)  # this is basically the document id number for that frequency

                        log_weight = 1 + math.log(tf) if tf > 0 else 0  # finding tf weight

                        idf_numerator = total_doc_number + 1  # Ensure numerator is greater than denominator
                        idf_denominator = word_doc_freq.get(word, 1)  # Avoid zero division
                        idf = math.log(idf_numerator / idf_denominator)  # Compute IDF safely

                        tf_idf_final_score = log_weight * idf  # this will be the final score of that word

                        # print(
                            # f"Doc {docID}: tf={tf}, tf_weight={log_weight}, idf_weight={idf}, tf-idf={tf_idf_final_score}")  # Debugging print

                        id_tf_word_map[docID] = tf_idf_final_score  # add this final score into the

                    refined_map[word] = id_tf_word_map
                    print(refined_map[word])
                    break

    # Ensure all words have at least one match before performing intersection
    if not refined_map:
        return []

    # Perform intersection to find common document IDs
    # common_doc_ids = set.intersection(*index_map.values())

    ranked_docs = defaultdict(float)
    for term, docs in refined_map.items():
        for doc_id, tf_idf in docs.items():
            ranked_docs[doc_id] += tf_idf  # Sum TF-IDF scores across query terms

    return sorted(ranked_docs.items(), key=lambda x: x[1], reverse=True)


def findURL(list_of_matches):
    doc_ids = {doc_id for doc_id, _ in list_of_matches}
    list_of_url = {}  # Use set to avoid duplicates

    with open(f'{ROOT_DIR}/url_id.txt', "r") as file:
        for line in file:
            id_line = re.match(r"(\d+):(.+)", line)

            if not id_line:
                continue

            doc_id = int(id_line.group(1))
            link = id_line.group(2)

            if doc_id in doc_ids:
                # print(f'This is working: {id_value}')
                list_of_url[link] = dict(list_of_matches).get(doc_id, 0)  # Store with score

                # Sort URLs based on TF-IDF scores
    return sorted(list_of_url.items(), key=lambda x: x[1], reverse=True)


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
