import pandas as pd
from pymongo import MongoClient
import glob2
import os
DIR_NAME = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(DIR_NAME, os.pardir))
IMAGES_PATH = os.path.join(ROOT, "data")
files= glob2.glob(f'{IMAGES_PATH}/*')


client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'AI_HCM_2023'
database = client[database_name]

# Access or create a collection
collection = database['collection']
collection.delete_many({})

# df_object = pd.read_pickle('df_object.pkl')
# df_color = pd.read_pickle('df_color.pkl')
# df = df_object.join(df_color)
# print(df)
df_color = pd.read_csv("./csv/fullColorsallBatch.csv", header=0)
df_object = pd.read_csv("./csv/Object_detection_final.csv", header=0)

for index, value in enumerate(files):
    colors_value = df_color['colors'][index]  # Assuming the column name is 'colors'
    colors = [color.strip().strip(" '{}'") for color in colors_value.split(',')]
    objects = df_object['results'][index]


    dict_objects = {}
    try:
        for object in objects.split(','):
            if len(object) > 0:
                key = object.split(":")[0].strip()
                value_object = int(object.split(":")[1].strip())
                if value_object > 5:
                    value_object = 5
                dict_objects[key] = value_object
        document = {
            "_id" : index,
            "image_link": value,
            "color": colors,
            "object": dict_objects
        }
    except:
        document = {
            "_id" : index,
            "image_link": value,
            "color": colors,
            "object": {}
        }

    collection.insert_one(document)

for doc in (collection).find({}):
    print(doc)

print(collection.count_documents({}))

client.close()