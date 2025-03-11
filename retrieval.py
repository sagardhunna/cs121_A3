import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import os
import math
from google import genai
from collections import defaultdict
import time

# Get the absolute path to the root CS121 directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # CS121

# Construct the absolute path to partial_indexes folder
PARTIAL_INDEXES_DIR = os.path.join(ROOT_DIR, "partial_indexes")

ai_docs = list()

def doc_count():
    count = 0
    with open(f'{ROOT_DIR}/total_count.txt', "r") as file:
        total_docs = file.readline()
    return int(total_docs)


TOTAL_DOCS = doc_count()


def find_shortest_list_key(my_map):
    min_length = float('inf')  # Initialize with a large value to ensure first iteration updates
    min_key = None

    for key, list_value in my_map.items():
        if len(list_value) < min_length:
            min_length = len(list_value)
            min_key = key

    return min_key, min_length


def normalize_word(word):
    word = word.lower()
    word = re.sub(r"[^\w\s]", "", word)  # removes apostrophes and special chars
    return word


def get_stop_words():
    stop_words = set()
    stemmer = PorterStemmer()

    with open(f'{ROOT_DIR}/english_stopwords.txt', "r", encoding='utf-8') as file:
        for word in file:
            word_clean = normalize_word(word.strip())
            if word_clean:
                stop_words.add(word_clean)

    return stop_words

def filter_stop_words(search):
    search = search.lower()
    word_set = set(search.strip().split(" "))  # split query into words
    stop_word_list = get_stop_words()

    clean_search_words = set()

    for word in word_set:
        norm_word = normalize_word(word)
        if norm_word not in stop_word_list:
            clean_search_words.add(norm_word)

    if clean_search_words:
        return clean_search_words
    else:
        return word_set

# this function is designed to make it more efficient to retrieve which partial index we should use to look for the term
# it will basically check the first letter in the word and search the document that matches that letter
def find_partial_file(searched_word):
    global ai_docs
    stemmer = PorterStemmer()

    #  implement filter_stop_words here

    word_list = filter_stop_words(searched_word)

    if not word_list:
        print("Empty search query. No terms to search.")
        return []

    word_doc_freq = {}
    refined_map = {}  # this will have a map that contains word: {docID: score}

    for word in word_list:  # checks each query word
        word = stemmer.stem(word.lower())
        if not word:
            continue
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

                        idf_numerator = TOTAL_DOCS + 1  # Ensure numerator is greater than denominator
                        idf_denominator = word_doc_freq.get(word, 1)  # Avoid zero division
                        idf = math.log(idf_numerator / idf_denominator)  # Compute IDF safely

                        tf_idf_final_score = log_weight * idf  # this will be the final score of that word

                        # print(
                            # f"Doc {docID}: tf={tf}, tf_weight={log_weight}, idf_weight={idf}, tf-idf={tf_idf_final_score}")  # Debugging print

                        id_tf_word_map[docID] = tf_idf_final_score  # add this final score into the

                    refined_map[word] = id_tf_word_map
                    #print(refined_map[word])
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
    
    top_links = []
    for i in range(0,5): #find top 5
        max_item = max(ranked_docs.items(), key=lambda x: x[1])
        top_links.append(max_item)
        ai_docs.append(max_item[0])
        ranked_docs.pop(max_item[0])
    return top_links


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

    return list_of_url.items()

def aiSum(filenumber):
    # textToSum = ""
    # url_map = dict()
    # file_number = 0
    # for dirpath, dirnames, filenames in os.walk("developer"):
    #     for filename in filenames:
    #         actual_rel_name = os.path.join(dirpath, filename)
    #         if '.json' not in actual_rel_name:
    #             continue
    #         with open(actual_rel_name, "r") as file:
    #             jsonObj = json.load(file)
    #             url = jsonObj.get("url").split("#")[0]
    #             if url in url_map.values():
    #                 continue
    #             soup = BeautifulSoup(httpsContent, features="html.parser")
    #             visible_text = soup.getText(" ")
    #             if len(visible_text) < 100:
    #                 continue
    #             if filenumber == (file_number+1):
    #                 client = genai.Client(api_key="AIzaSyC-muWK1XQU_j5B7pIhC5BZOPTmVBjSqzA")
    #                 response = client.models.generate_content(
    #                     model="gemini-2.0-flash",
    #                     contents=textToSum,
    #                 )
    #                 return response.text
    #             file_number += 1
    #             print(file_number)
    return "error with summary"


def make_query(query):
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
    global ai_docs
    for i in range(4):
        word = input("Please enter a search query: ")
        start = time.perf_counter() #tests how long the code takes to execute
        matched_ids = find_partial_file(word)
        end = time.perf_counter()
        print(f'runtime: {end-start} seconds')
        # print("Here are the overlapping strings: ")
        # print(matched_ids)
        count = 0
        for links in findURL(matched_ids):
            if count == 5:
                break
            print(links)
            print(aiSum(ai_docs[count]))
            count += 1


if __name__ == "__main__":
    main()
