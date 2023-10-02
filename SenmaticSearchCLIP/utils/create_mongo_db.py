# import pymongo
# # mongodb+srv://root:root@cluster0.yqk9xiu.mongodb.net/

# from pymongo import MongoClient
# CONNECTION_STRING = "mongodb+srv://root:root@cluster0.yqk9xiu.mongodb.net/"
# # def get_database():
 
# #    # Provide the mongodb atlas url to connect python to mongodb using pymongo
# #    CONNECTION_STRING = "mongodb+srv://root:root@cluster0.yqk9xiu.mongodb.net/"
 
# #    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
# #    client = MongoClient(CONNECTION_STRING)
 
# #    # Create the database for our example (we will use the same database throughout the tutorial
# #    return client['post']
  
# # # This is added so that many files can reuse the function get_database()
# # if __name__ == "__main__":   
  
# #    # Get the database
# #    dbname = get_database()
# print("Successfully connected")

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

import os
import glob2
DIR_NAME = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(DIR_NAME, os.pardir))
IMAGES_PATH = os.path.join(ROOT, "data")

files= glob2.glob(f'{IMAGES_PATH}/*')

# Access or create a database
database_name = 'HCM_AI_2023'
database = client[database_name]

# Access or create a collection
collection_name = 'images'
collection = database[collection_name]

for index, row in enumerate(files):
    document = {"image_path": row, f'{object[0]}': object[1]}
    collection.insert_one(document).inserted_id

# Close the MongoDB connection
client.close()
print('okiii')
#############
object = [
    {"results": "airplane: 2, person: 7, skis: 1, oven: 1, bicycle: 2, clock: 1, train: 2, snowboard: 1, scissors: 1, car: 1, tv: 2, bird: 1, boat: 1, surfboard: 1"}
]

json_data = {"id": 0, "image_path": "row"}  # Create a dictionary to store the objects

for i in object:
    result_split = i["results"].split(",")
    for j in result_split:
        obj_split = j.split(":")
        obj_key = obj_split[0].strip()  # Remove any whitespace from the key
        obj_value = obj_split[1].strip()  # Remove any whitespace from the value

        json_data[obj_key] = obj_value  # Add the object key-value pair to the dictionary

# Convert json_data to JSON format
import json

json_string = json.dumps(json_data)
print(json_string)

# Define the search query
search_query = {
    "$or": [
        {"about": {"$regex": "similarity in comparison", "$options": "i"}},
        {"categories": {"$regex": "similarity in comparison", "$options": "i"}}
    ]
}

# Define the projection and sort
projection = {
    "object": -1,
    "place": -1,
    "searchScore": {"$meta": "textScore"}
}

sort = [("searchScore", {"$meta": "textScore"})]

# Execute the aggregation
result = collection.aggregate([
    {"$match": search_query},
    {"$project": projection},
    {"$sort": sort}
])

# Print the sorted documents
for doc in result:
    print(doc)