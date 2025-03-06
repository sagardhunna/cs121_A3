import os
import operator
import time

def merge_duplicates():
    files = list() #list of the rough index filedumps to open
    streams = list() #list of the io filestreams to create the iterators from 
    iterWords = list() # basically just a list of 2 element lists where the first element is the current line
                       # and the second element is the iterator we used to grab that line 

    write_file = open("partial_indexes/partial_index_0.txt","wt") #first file to write to
    
    filenum = 1
    while True: # loops through the directory of rough indexes in numeric order to grab their names
        if os.path.exists(f"rough_indexes/rough_ind_{filenum}.txt"):
            file_path = os.path.join(f"rough_indexes/rough_ind_{filenum}.txt")
            files.append(file_path)
        else:
            break
        filenum+=1

    for f in files: #creates our list of io filestreams
        streams.append(open(f, "r", 1, encoding="utf-8"))

    for s in streams: #creates our list of mini lists that have the line of text and iterator
        temp = list()
        it = iter(s)
        temp.append(next(it))
        temp.append(it)
        iterWords.append(temp)

    iterWords.sort(key=operator.itemgetter(0)) #sorts the list to make sure the first element is the first lexicographically
    #used itemgetter because it's faster than a lambda function according to what i read online (and tested)
    
    count = 0 #keeps track of unique token count
    prev_ltr = "0" #keeps track of the current letter/digit we're on to make sure we are writing to the correct partial index
    

    #loops through every single rough index dump one line at a time so we don't load everything into memory at once.
    #we simply visit each line of each file once, which is as efficient as it gets. 
    # basically a multi-array (rather than 2) implementation of the merge algorithm from the discussion in week 3 or whenever it was
    while iterWords: 
        count+=1

        if len(iterWords)==1: #if there's only one iterator left, we can just print out the remaining lines from that file
            write_file.write(iterWords[0][0].strip())
            try:
                iterWords[0][0] = next(iterWords[0][1])
            except StopIteration:
                iterWords.clear()
                break
            continue

#the reason we sort the array after every pass is because:
# 1. python's sort function is INCREDIBLY fast for partially sorted arrays, and our list is almost always partially sorted to a decent amount.
# 2. having it sorted allows us to take advantage of some optimizations when reading the lines, mostly early exits and significantly less comparisons.
# it overall makes the code MUCH cleaner and we can rely on them being in sorted order when writing as well, which keeps our merged invertex index in 
# order as well.
        iterWords.sort(key=operator.itemgetter(0)) 


        currLine = iterWords[0][0].strip()
        word = currLine[:currLine.find(" ")] #gets the actual token from the whole line

        if prev_ltr != word[0]: #if our letter is new, change the write destination to the correct partial file
            write_file.close() # this is ONLY triggered once we are completely through one letter, so no waste with file opens.
            write_file = open(f"partial_indexes/partial_index_{word[0]}.txt","wt")
            prev_ltr = word[0]

        to_remove = list() #builds a list to keep track of which iterators we have to remove if they reach EOF(if any)
        for i in range(1,len(iterWords)):
            linei = iterWords[i][0].strip()
            if word != linei[:linei.find(" ")]: #since the list is sorted, we can exit early if we find a token that differs
                break
            currLine = currLine + linei[len(word):] #otherwise, we can combine our current line of token freq/weight with the one we just found
            try:
                iterWords[i][0] = next(iterWords[i][1])
            except StopIteration:
                to_remove.append(i)
        try:
            iterWords[0][0] = next(iterWords[0][1])
        except StopIteration: #update the first item (2-element list, technically) in out list of line,iterator values
            to_remove.insert(0,0)
        for i in reversed(to_remove): #removes any EOF iterator from the iterWords list, so we don't have to keep track of it anymore
            iterWords.pop(i)
        write_file.write(currLine+"\n")
            

    for s in streams: #make sure to close all filestreams after we're done
        s.close()
    write_file.close()
    return count #return unique token count

def main():
    start = time.perf_counter() #tests how long the code takes to execute
    for i in range(0,1):
        count = merge_duplicates()
    end = time.perf_counter()
    print(f'runtime: {end-start} seconds')
    print(f'unique tokens: {count}')


if __name__ == "__main__":
    main()
