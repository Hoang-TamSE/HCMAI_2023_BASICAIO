import pandas as pd
from pymongo import MongoClient

def get_image_path_by_index(index):
    client = MongoClient('mongodb://localhost:27017/')

    # Access or create a database
    database_name = 'AI_HCM_2023'
    database = client[database_name]

    # Access or create a collection
    collection = database['collection']

    # Fetch the document by index from the collection
    document = collection.find_one({'_id': index})

    # Extract the image path from the document
    image_path = document['image_link']

    client.close()

    return image_path

print(get_image_path_by_index(1113586))