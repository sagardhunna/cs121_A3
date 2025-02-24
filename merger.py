# open all three partial index files so we can iterate through them
with open("partial_index_1", "r", 1) as file1, open("partial_index_1", "r", 1) as file2, open("partial_index_1", "r", 1) as file3:
    # creates an iterator for each file that we will use to loop through each file
    part1 = iter(file1)
    part2 = iter(file2)
    part3 = iter(file3)
    switch1 = True
    switch2 = True
    switch3 = True
    line1 = ""
    line2 = ""
    line3 = ""
    while True:
        try:
            if switch1:
                line1 = next(part1).strip()
        except StopIteration:
            line1 = ""

        try:
            if switch2:
                line2 = next(part2).strip()
        except StopIteration:
            line1 = ""

        try:
            if switch3:
                line3 = next(part3).strip()
        except StopIteration:
            line1 = ""
        
        if not line1 and not line2 and not line3:
            break