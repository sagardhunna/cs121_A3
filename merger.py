import os
import re
import operator

folder_path = "rough_indexes"

count = 0

def merge_duplicates():
    files = list()
    streams = list()
    iterWords = list()
    write_file = open("merged_index.txt","wt")
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            files.append(file_path)
    for f in files:
        streams.append(open(f, "r", 1, encoding="utf-8"))
    prio = 0
    for s in streams:
        temp = list()
        it = iter(s)
        temp.append(next(it))
        temp.append(it)
        temp.append(prio)
        iterWords.append(temp)
        prio+=1
    iterWords.sort(key=operator.itemgetter(0,2))

    while len(iterWords) > 0:

        if len(iterWords)==1:
            write_file.write(iterWords[0][0].strip())
            try:
                iterWords[0][0] = next(iterWords[0][1])
            except StopIteration:
                iterWords.remove(iterWords[i])
            continue

        if iterWords[0][0] > iterWords[1][0]:
            iterWords.sort(key=operator.itemgetter(0,2))
        stop_pt = 0
        currLine = iterWords[0][0].strip()
        word = currLine.split()[0]
        for i in range(1,len(iterWords)):
            stop_pt+=1
            if(word != iterWords[i][0].strip().split()[0]):
                break
        for i in range(1,stop_pt):
            currLine = currLine + iterWords[i][0].strip()[len(word):]
        write_file.write(currLine+"\n")
        for i in range(0,stop_pt):
            try:
                iterWords[i][0] = next(iterWords[i][1])
            except StopIteration:
                iterWords.remove(iterWords[i])
                i-=1

    for s in streams:
        s.close()
    write_file.close()

def main():
    merge_duplicates()


if __name__ == "__main__":
    main()
