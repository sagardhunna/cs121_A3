import os
for dirpath, dirnames, filenames in os.walk("developer"):
    for filename in filenames:
        actual_rel_name = os.path.join(dirpath, filename)
