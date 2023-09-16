import mysql.connector
import os
import glob2
import json
METADATA_PATH = "metadata"



files= glob2.glob(f'{METADATA_PATH}/*')
metadata_name = "metadata.json"
dict_file = {}
for file_path in files:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        file_name = file_path.split("\\")[1].split(".")[0]
        dict_file[file_name] = data['watch_url']

with open(metadata_name, "w") as file:
    json.dump(dict_file, file)

