import os

# this function is designed to make it more efficient to retrieve which partial index we should use to look for the term
# it will basically check the first word in the file and if the word is larger than the searched word currently at hand
# it adds the document into a map with the word for the designated file,
def find_partial_file(searched_word):
    word_list = searched_word.split(" ") # splits search into seperate words
    index_map = {} # map to return
    print(word_list)
    for word in word_list: # checks each query word
        for dirpath, dirnames, filenames in os.walk("partial_indexes"): # need to fix this taken from indexer
            for filename in sorted(filenames):
                actual_rel_name = os.path.join(dirpath, filename)
                print(f'File we are looking at: File {actual_rel_name}')
                with open(actual_rel_name, "r", encoding= "utf-8") as current_doc: # opening the current doc
                    first_line = current_doc.readline().strip() # cleaning and reading the first line of the doc
                    first_word = first_line.split(" ")[0] if first_line else "" #takes to see the first word
                    print(f'This is the first word:  + {first_word}')

                if word < first_word: #if the query word is less than the first word of that document it will assign prev map
                    index_map[word] = actual_rel_name
                    break #stops the loop because word was found in prev doc existence
            break

# def find_query(word):





def main():
    word = "This is so gay"
    find_partial_file(word)


if __name__ == "__main__":
    main()
