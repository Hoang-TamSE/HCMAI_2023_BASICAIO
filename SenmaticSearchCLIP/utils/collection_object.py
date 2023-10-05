import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'test_db'
database = client[database_name]

# Access or create a collection
collection_object = database['collection_object']

# Read the CSV file and convert the result column to a dictionary
filename = "resultFas_rcnn - resultFas_rcnn.csv"
collection_object.delete_many({})

df = pd.read_csv(filename)

for index, row in df.iterrows():
    image_link = row['image_link']
    results = row['results']
    
    dict_objects = {}
    try:
        for object in results.split(','):
            if len(object) > 0:
                key = object.split(":")[0].strip()
                value = int(object.split(":")[1].strip())
                dict_objects[key] = value
    
        document = {
            "image_link": image_link,
            "result": dict_objects
        }
    except:
        document = {
            "image_link": image_link,
            "result": {}
        }
    collection_object.insert_one(document)
    

for doc in collection_object.find({}):
    print(doc)


collection_object.count_documents({})

client.close()