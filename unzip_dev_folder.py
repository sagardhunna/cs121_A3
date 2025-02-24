import zipfile
with zipfile.ZipFile("developer.zip", 'r') as zip_file:
    zip_file.extractall("developer")