# open all three partial index files so we can iterate through them
with open("partial_indexes/partial_index_1.txt", "r", encoding="utf-8") as file1, open("partial_indexes/partial_index_2.txt", "r", encoding="utf-8") as file2, open("partial_indexes/partial_index_3.txt", "r", encoding="utf-8") as file3:
    writer = open("inverse_index","wt")
    # create an iterator for each file that we will use to loop through each file
    part1 = iter(file1)
    part2 = iter(file2)
    part3 = iter(file3)

    #create three boolean switches to keep track of EOF iterator
    switch1 = False
    switch2 = False
    switch3 = False

    #init 3 strings that will store a line from each file
    line1 = next(part1)
    line2 = next(part2)
    line3 = next(part3)

    count = 0

    #loop until EOF on all files
    while True:
        print(f'Count: {count}')
        if switch1 and switch2 and switch3:
            print("finished?")
            break
        
        count += 1
        # set all words to be blank becuase once we are end of file, we do no want to split the string anymore
        word1 = ""
        word2 = ""
        word3 = ""

        if line1 != "":
            word1 = line1.split()[0]
        if line2 != "":
            word2 = line2.split()[0]
        if line3 != "":
            word3 = line3.split()[0]

        print(f'Word1: {word1} -- Word2: {word2} -- Word3: {word3}')

        if word1!="":
            if word1 < word2 and word1 < word3:
                writer.write(line1)
                try:
                    line1 = next(part1).strip()
                except StopIteration:
                    line1 = ""
                    switch1 = True
                continue
        if word2!="":
            if word2 < word1 and word2 < word3:
                writer.write(line2)
                try:
                    line2 = next(part2).strip()
                except StopIteration:
                    line2 = ""
                    switch2 = True
                continue
        if word3!="":
            if word3 < word1 and word3 < word2:
                writer.write(line3)
                try:
                    line3 = next(part3).strip()
                except StopIteration:
                    line3 = ""
                    switch3 = True
                continue
        
        if word1 != "":
            if word1==word2:
                if word1==word3: #1==2==3
                    writer.write(line1+line2[len(word2):]+line3[len(word3):])
                    try:
                        line1 = next(part1).strip()
                    except StopIteration:
                        line1 = ""
                        switch1 = True

                    try:
                        line2 = next(part2).strip()
                    except StopIteration:
                        line2 = ""
                        switch2 = True

                    try:
                        line3 = next(part3).strip()
                    except StopIteration:
                        line3 = ""
                        switch3 = True
                    continue
            else: #1==2
                writer.write(line1+line2[len(word2):])
                try:
                    line1 = next(part1).strip()
                except StopIteration:
                    line1 = ""
                    switch1 = True
                    
                try:
                    line2 = next(part2).strip()
                except StopIteration:
                    line2 = ""
                    switch2 = True
                continue
        
            if word1==word3: #1==3
                writer.write(line1+line3[len(word3):])
                try:
                    line1 = next(part1).strip()
                except StopIteration:
                    line1 = ""
                    switch1 = True
                
                try:
                    line3 = next(part3).strip()
                except StopIteration:
                    line3 = ""
                    switch3 = True
                continue
            
            if word2==word3: #2==3
                writer.write(line2+line3[len(word3):])
                try:
                    line2 = next(part2).strip()
                except StopIteration:
                    line2 = ""
                    switch2 = True

                try:
                    line3 = next(part3).strip()
                except StopIteration:
                    line3 = ""
                    switch3 = True
                continue
        if word1 > word2 and word1 > word3:
            writer.write(line1)
            try:
                line1 = next(part1).strip()
            except StopIteration:
                line1 = ""
                switch1 = True
            continue

        if word2 > word1 and word2 > word3:
            writer.write(line2)
            try:
                line2 = next(part2).strip()
            except StopIteration:
                line2 = ""
                switch2 = True
            continue
        
        if word3 > word1 and word3 > word2:
            writer.write(line3)
            try:
                line3 = next(part3).strip()
            except StopIteration:
                line3 = ""
                switch3 = True
            continue
    writer.close()
    print(count)