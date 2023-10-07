import pandas as pd
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
database_name = 'AI_HCM_2023'
database = client[database_name]

collection = database['collection']

def get_image_path_by_index(index):

    # Access or create a database
    

    # Fetch the document by index from the collection
    document = collection.find_one({'_id': index})
    # Extract the image path from the document
    image_path = document['image_link']


    return image_path

def search_objects_and_colors(user_input, idx):
    # Create a list to hold the conditions for the "object" column
    object_conditions = []
    results = []
    
    # Build the conditions for the "object" column based on user input
    for key, value in user_input.items():
            if key != 'color':
                condition = {f"object.{key}": value}
                object_conditions.append(condition)
    
    # Create a list to hold the conditions for the "colors" column
    color_conditions = []
    
    # Build the conditions for the "color" column based on user input
    for color in user_input.get("color", []):
        if color != "":
            condition = {"color": color}
            color_conditions.append(condition)
    
    # Combine the conditions for "object" and "colors" using "$or" operator
    for i in idx:
        if len(color_conditions) > 0 and len(object_conditions) > 0:
            query_conditions = {
                "$and": [
                    {"$and": object_conditions},
                    {"$or": color_conditions},
                    {"_id": int(i)}
                ]
            }
        elif len(color_conditions) > 0:
            query_conditions = {
                "$and": [
                    {"$or": color_conditions},
                    {"_id": int(i)}
                ]
            }
        elif len(object_conditions) > 0:
            query_conditions = {
                "$and": [
                    {"$and": object_conditions},
                    {"_id": int(i)}
                ]
            }
        else:
            query_conditions = [
                {"_id": int(i)}
            ]
        print(query_conditions)
        result = collection.find(query_conditions)
        results.extend(result)

     # Store the image_link values in a list
    indexes = [doc["_id"] for doc in results]
    
    return indexes[0:1000]

