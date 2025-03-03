import os
import re

folder_path = "rough_indexes"

output_folder = "partial_indexes"

os.makedirs(output_folder, exist_ok=True) # making sure it exists

letter_map = {}
count = 0

def merge_duplicates():
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                for line in file:
                    line = line.lstrip()
                    match = re.search(r"^\S+", line)  # searches all words in a space
                    word = match.group(0) if match else None  # finds the first one

                    if word is None:
                        continue

                    docs = re.findall(r"(doc\d+,\d+)", line)  # checks the doc1,1

                    if word not in letter_map.keys():
                        letter_map[word] = set(docs)  # starts the map
                    else:
                        letter_map[word].update(docs)  # Append list of docs

        sorted_letter_map = {
            word: sorted(docs, key=lambda doc: int(re.search(r"doc(\d+)", doc).group(1)))
            for word, docs in sorted(letter_map.items())
        }

        for word, docs in sorted_letter_map.items():
            partial_file = os.path.join(output_folder, f"partial_index_{word[0]}.txt")

            with open(partial_file, "a") as file:
                file.write(f'{word}')
                for doc in docs:  # `docs` is a list of strings
                    file.write(f' {doc}')
                file.write('\n')

    letter_map.clear()


def main():
    merge_duplicates()


if __name__ == "__main__":
    main()
