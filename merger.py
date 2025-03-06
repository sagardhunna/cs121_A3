import os
import operator
import time

def merge_duplicates():
    files = list()
    streams = list()
    iterWords = list()
    write_file = open("partial_indexes/partial_index_0.txt","wt")
    filenum = 1
    while 1:
        if os.path.exists(f"rough_indexes/rough_ind_{filenum}.txt"):
            file_path = os.path.join(f"rough_indexes/rough_ind_{filenum}.txt")
            files.append(file_path)
        else:
            break
        filenum+=1
    for f in files:
        streams.append(open(f, "r", 1, encoding="utf-8"))
    for s in streams:
        temp = list()
        it = iter(s)
        temp.append(next(it))
        temp.append(it)
        iterWords.append(temp)

    iterWords.sort(key=operator.itemgetter(0))
    
    count = 0
    prev_ltr = "0"
    while iterWords:
        count+=1

        if len(iterWords)==1:
            write_file.write(iterWords[0][0].strip())
            try:
                iterWords[0][0] = next(iterWords[0][1])
            except StopIteration:
                iterWords.clear()
                break
            continue

        iterWords.sort(key=operator.itemgetter(0))


        currLine = iterWords[0][0].strip()
        word = currLine[:currLine.find(" ")]

        if prev_ltr != word[0]: 
            write_file.close()
            write_file = open(f"partial_indexes/partial_index_{word[0]}.txt","wt")
            prev_ltr = word[0]

        word = currLine[:currLine.find(" ")]
        to_remove = list()
        for i in range(1,len(iterWords)):
            linei = iterWords[i][0].strip()
            if word != linei[:linei.find(" ")]:
                break
            currLine = currLine + linei[len(word):]
            try:
                iterWords[i][0] = next(iterWords[i][1])
            except StopIteration:
                to_remove.append(i)
        try:
            iterWords[0][0] = next(iterWords[0][1])
        except StopIteration:
            to_remove.insert(0,0)
        for i in reversed(to_remove):
            iterWords.pop(i)
        write_file.write(currLine+"\n")
            

    for s in streams:
        s.close()
    write_file.close()
    return count

def main():
    start = time.perf_counter()
    for i in range(0,1):
        count = merge_duplicates()
    end = time.perf_counter()
    print(f'runtime: {end-start} seconds')
    print(f'unique tokens: {count}')


if __name__ == "__main__":
    main()
