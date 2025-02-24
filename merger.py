# open all three partial index files so we can iterate through them
with open("partial_index_1", "r", 1, encoding="utf-8") as file1, open("partial_index_2", "r", 1, encoding="utf-8") as file2, open("partial_index_3", "r", 1, encoding="utf-8") as file3:
    
    # create an iterator for each file that we will use to loop through each file
    part1 = iter(file1)
    part2 = iter(file2)
    part3 = iter(file3)

    #create three boolean switches to keep track of changes to each iterator
    switch1 = True
    switch2 = True
    switch3 = True

    #init 3 strings that will store a line from each file
    line1 = ""
    line2 = ""
    line3 = ""

    #loop until EOF on all files
    while True:
        try:
            if switch1:
                line1 = next(part1).strip()
        except StopIteration:
            line1 = ""
            switch1 = False

        try:
            if switch2:
                line2 = next(part2).strip()
        except StopIteration:
            line2 = ""
            switch2 = False

        try:
            if switch3:
                line3 = next(part3).strip()
        except StopIteration:
            line3 = ""
            switch3 = False
        
        if not (line1 or line2 or line3):
            print("finished?")
            break
        
        word1 = line1.split[0]
        word2 = line2.split[0]
        word3 = line3.split[0]

        if word1 == word2